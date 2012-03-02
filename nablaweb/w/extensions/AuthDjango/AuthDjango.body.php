<?php
    /* AuthDjango.php */
    
    /**
     * This plugin allows you to use the django auth system with mediawiki.
     *
     * Copyright 2009-2010 Thomas Lilley <mail@tomlilley.co.uk> (tomlilley.co.uk)
     * Copyright 2011 Jack Grigg <me@jackgrigg.com> (jackgrigg.com)
     *
     * This program is free software; you can redistribute it and/or modify
     * it under the terms of the GNU General Public License as published by
     * the Free Software Foundation; either version 2 of the License, or
     * any later version.
     *
     * This program is distributed in the hope that it will be useful,
     * but WITHOUT ANY WARRANTY; without even the implied warranty of
     * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
     * GNU General Public License for more details.
     *
     * http://www.gnu.org/copyleft/gpl.html
     */

    /**
     * Not actually used for authentication, UserLoadFromSession does that.
     *
     */
    class AuthDjango extends AuthPlugin {
        /**
         * DatabaseMysql database object for Django
         *
         * @var object
         */
        private $dbd;
        
        /**
         * Users table name
         *
         * @var string
         */
        private $user_table;
        
        /**
         * Sesion table name
         *
         * @var string
         */
        private $session_table;
        
        /**
         * Session profile table name
         *
         * @var string
         */
        private $session_profile_table;
        
        /**
         * Connects to the database and inititaes some variables.
         *
         */
        public function __construct() {
            // Disable mediawiki account creation
            $GLOBALS['wgGroupPermissions']['*']['createaccount'] = false;
            
            // Set table names
            $this->authdjango_table         = $GLOBALS['wgAuthDjangoConfig']['AuthDjangoTable'];
            $this->user_table               = $GLOBALS['wgAuthDjangoConfig']['UserTable'];
            $this->session_table            = $GLOBALS['wgAuthDjangoConfig']['SessionTable'];
            $this->session_profile_table    = $GLOBALS['wgAuthDjangoConfig']['SessionprofileTable'];
            
            // start database connection
            $this->dbd = new DatabaseMysql(
                $GLOBALS['wgAuthDjangoConfig']['DjangoHost'],
                $GLOBALS['wgAuthDjangoConfig']['DjangoUser'],
                $GLOBALS['wgAuthDjangoConfig']['DjangoPass'],
                $GLOBALS['wgAuthDjangoConfig']['DjangoDBName']
            );
            
            // Set hooks functions
            $GLOBALS['wgHooks']['UserLogout'][]            = $this;
            $GLOBALS['wgHooks']['UserLoadFromSession'][]   = $this;
            $GLOBALS['wgHooks']['PersonalUrls'][]          = $this;
        }
        
        /**
         * Check whether there exists a user account with the given name.
         * The name will be normalized to MediaWiki's requirements, so
         * you might need to munge it (for instance, for lowercase initial
         * letters).
         *
         * @param $username String: username.
         * @return bool
         */
        public function userExists($username) {
            // Since if a user does not exist they will be created,
            // always return true.
            return true;
        }
        
        /**
         * Return true if the wiki should create a new local account automatically
         * when asked to login a user who doesn't exist locally but does in the
         * external auth database.
         *
         * If you don't automatically create accounts, you must still create
         * accounts in some way. It's not possible to authenticate without
         * a local account.
         *
         * This is just a question, and shouldn't perform any actions.
         *
         * @return bool
         */
        public function autoCreate() {
            return true;
        }

        /**
         * Can users change their passwords?
         *
         * @return bool
         */
        public function allowPasswordChange() {
            return false;
        }

        /**
         * Set the given password in the authentication database.
         * As a special case, the password may be set to null to request
         * locking the password to an unusable value, with the expectation
         * that it will be set later through a mail reset or other method.
         *
         * Return true if successful.
         *
         * @param $user User object.
         * @param $password String: password.
         * @return bool
         */
        public function setPassword( $user, $password ) {
            return false;
        }
        
        /**
         * Return true to prevent logins that don't authenticate here from being
         * checked against the local database's password fields.
         *
         * This is just a question, and shouldn't perform any actions.
         *
         * @return bool
         */
        public function strict() {
            return true;
        }

        /**
         * Check if a user should authenticate locally if the global authentication fails.
         * If either this or strict() returns true, local authentication is not used.
         *
         * @param $username String: username.
         * @return bool
         */
        public function strictUserAuth( $username ) {
            return true;
        }
        
        /**
         * Login in to mediawiki from an existing django session.
         * User must be logged in to django for this to work.
         *
         * @param object $user
         * @param bool $result
         * @return bool
         */
        public function onUserLoadFromSession($user, &$result) {
            global $wgLanguageCode, $wgRequest, $wgOut;
            $lg = Language::factory($wgLanguageCode);
            if (isset($_REQUEST['title']) && strstr($_REQUEST['title'], $lg->specialPage('Userlogin'))) {
                // Redirect to our login page
                $returnto = $wgRequest->getVal('returnto');
                // Don't redirect straight back to the logout page
                $returnto = (strstr($returnto, $lg->specialPage('Userlogout'))) ? '' : $returnto;
                $wgOut->redirect($GLOBALS['wgAuthDjangoConfig']['LinkToSiteLogin'] . '?next=' . $GLOBALS['wgAuthDjangoConfig']['LinkToWiki'] . $returnto);
            } elseif (array_key_exists('sessionid', $_COOKIE)) {
                $django_session = $_COOKIE['sessionid'];

                // find if there is a user connected to this session
                $r1 = $this->dbd->selectRow(
                    array(
                        $this->user_table,
                        $this->session_profile_table
                    ),
                    array(
                        $this->user_table . '.id AS d_user_id',
                        'username',
                        'email'
                    ),
                    array(
                        $this->user_table . '.id=user_id',
                        'session_id' => $django_session
                    )
                );

                if ($r1) {
                    // there is a Django session present
                    $user_id = $r1->d_user_id;
                    $dbr = wfGetDB(DB_SLAVE);
                    $mw_uid = $dbr->selectField(
                        $this->authdjango_table,
                        'mw_user_id',
                        array(
                            'd_user_id' => $user_id
                        )
                    );

                    $local_id = ($mw_uid) ? $mw_uid : 0;

                    if (!$mw_uid) {
                        // Django user does not exist in MW djangouser table
                        // create a new user if one does not exist, and update
                        // djangouser table if one does
                        $username = $r1->username;
                        $email = $r1->email;

                        // replace space with underscore
                        // (site login doesn't allow spaces in usernames)
                        $username = str_replace(' ', '_', $username);
                        $u = User::newFromName($username);
                        if ($u->getID() == 0) {
                            // FIXME: Is the AuthDjango::userExists call necessary here?
                            if (AuthDjango::autoCreate() && AuthDjango::userExists($username)) {
                                $u->setEmail($email);
                                $u->confirmEmail();
                                $u->addToDatabase();
                                $u->setToken();
                            }
                        }
                        // Either a new MW user hs been created or there was an existing
                        // user with the same (ignoring spaces) username.
                        // In any case, update authdjango table.
                        $local_id = $u->getID();
                        $dbw = wfGetDB(DB_MASTER);
                        $dbw->insert(
                            $this->authdjango_table,
                            array(
                                'd_user_id' => $user_id,
                                'mw_user_id' => $local_id
                            )
                        );
                    }
                    
                    $user->setID($local_id);
                    $user->loadFromId();
                    $result = true;
                    $user->setCookies();
                    wfSetupSession();
                } else {
                    // if we're not logged in on the site make sure we're logged out of the database.
                    setcookie('wikidb_session', '', time()-3600);
                    unset($_COOKIE['wikidb_session']);
                    if (session_id() != "") {
                        session_destroy();
                    }
                }
            } else {
                // if we're not logged in on the site make sure we're logged out of the database.
                setcookie('wikidb_session', '', time()-3600);
                unset($_COOKIE['wikidb_session']);
                if (session_id() != "") {
                    session_destroy();
                }
            }
            
            return true;
        }
        
        /**
         * Logs user out of django
         *
         * @param object $user
         * @return bool
         */
        public function onUserLogout(&$user) {
            if (array_key_exists('sessionid', $_COOKIE)) {
                // Delete session from session table and session profile table
                $this->dbd->delete(
                    $this->session_table,
                    array(
                        'session_key' => $_COOKIE['sessionid']
                    )
                );
                $this->dbd->delete(
                    $this->session_profile_table,
                    array(
                        'session_id' => $_COOKIE['sessionid']
                    )
                );
            }
            
            // Clear cookies and session data
            setcookie('sessionid', '', time()-3600);
            unset($_COOKIE['sessionid']);
            if (session_id() != "") {
                session_destroy();
            }
            return true;
        }
        
        /**
         * Unset anonymous login.
         *
         * @param object $personal_urls
         * @param object $wgTitle
         * @return bool
         */
        public function onPersonalUrls($personal_urls, $wgTitle) {
            unset( $personal_urls['anonlogin'] );
            return true;
        }
    }
