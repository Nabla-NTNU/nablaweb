// main.js begins
require(
  {
    baseUrl: '/static/',
    packages: [{
      name: 'physicsjs',
      location: 'PhysicsJS/dist',
      main: 'physicsjs.min'
    }]
  },
  [
  'require',
  'physicsjs',
  
  // official modules
  'physicsjs/renderers/dom',
  'physicsjs/bodies/circle',
  'physicsjs/bodies/rectangle',
  'physicsjs/bodies/convex-polygon',
  'physicsjs/behaviors/newtonian',
  'physicsjs/behaviors/sweep-prune',
  'physicsjs/behaviors/body-collision-detection',
  'physicsjs/behaviors/body-impulse-response',
  'physicsjs/behaviors/constant-acceleration'
], function(
  require,
  Physics
){
  var par = $('body').get(0);
  try {
    par && par.innerWidth;
  } catch( e ){
    par = window;
  }

  var renderer = Physics.renderer('dom', {
    el: 'viewport',
    width: par.innerWidth,
    height: par.innerHeight,
    // meta: true,
    debug:true,
    styles: {
      'circle': {
        strokeStyle: 'rgb(0, 30, 0)',
        lineWidth: 1,
        fillStyle: 'rgb(100, 200, 50)',
        angleIndicator: false
      },
      'rectangle': {
        strokeStyle: 'rgb(0, 0, 0)',
        lineWidth: 1,
        fillStyle: 'rgb(100, 200, 50)',
        angleIndicator: true
      },
      'convex-polygon' : {
        strokeStyle: 'rgb(60, 0, 0)',
        lineWidth: 1,
        fillStyle: 'rgb(60, 16, 11)',
        angleIndicator: false
      }
    }
  });
  
  window.addEventListener('resize', function(){
    renderer.el.width = par.innerWidth;
    renderer.el.height = par.innerHeight;
  });
  
  var init = function init( world, Physics ){
  
    var ship = Physics.body('circle', {
      x: 50,
      y: 50,
      vx: 0.08,
      radius: 30
    });
    ship.view = new Image();
    ship.view.src = require.toUrl('/media/advent/bag.png');

    var ground = Physics.body('rectangle', {
      fixed: true,
      x: 0,
      y: 50,
      width: 300,
      height: 10,
      treatment: "static",
      style: {
        strokeStyle: 'rgb(0, 0, 0)',
        lineWidth: 1,
      }
    });
    // bodies

    
    // render on every step
    world.on('step', function(){
      world.render();
    });

    // controls
    $(par).on('mouse-move', function(e) {
      ship.position.x = e.x;
      ship.position.y = e.y;
    });
    
    // add things to the world
    world.add([
      ship,
      ground,
      Physics.behavior('newtonian', { strength: 1e-4 }),
      Physics.behavior('sweep-prune'),
      Physics.behavior('body-collision-detection'),
      Physics.behavior('body-impulse-response'),
      Physics.behavior('constant-acceleration', { acc: {y: 1e-4, x: 0} }),
      renderer
    ]);

    for (i = 0; i < 5; i++) {
      for (j = 0; j < 5; j++) {
        var gift = Physics.body('circle', {
          mass: 10,
          radius: 10,
          x: j*10,
          y: i*10,
        });
        gift.view = new Image();
        gift.view.src = require.toUrl('/media/advent/gift.png');
        world.add(gift);
      }
    }
  };
  
  var world = null;
  var newGame = function newGame(){
    
    if (world){
      world.destroy();
    }
    
    world = Physics( init );
    world.on('lose-game', function(){
      document.body.className = 'lose-game';
      inGame = false;
    });
    world.on('win-game', function(){
      world.pause();
      document.body.className = 'win-game';
      inGame = false;
    });
  };

  // Game controls
  $('#start').click(newGame);
  $('#viewport').click(function (e) {
     // bodies

  });
  $('#gift').click(function (e) {
     // bodies
    world.pause();
  });




  // subscribe to ticker and start looping
  Physics.util.ticker.on(function( time ){
    if (world){
      world.step( time ); 
    }
  }).start();
})