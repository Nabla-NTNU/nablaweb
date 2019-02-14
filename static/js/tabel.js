"use strict";

/*** README ***\
* TODO: write a better readme
* header must include:
  - id=tabel-name
    EXAMPLE: id="tabel-name"
  - data-type=[boolean, string]
    EXAMPLE: data-type="boolean"
  - data-sort-by=[first:order,second:order,...]
    EXAMPLE: data-sort-by="bio:asc,name:dec"
    NOTE: order is either 'asc' or 'desc'

* cells must include:
  - boolean: non-empty is true, empty is false
  - string: any textvalue

TODO: Add support for numeric values, or simple fallback support with <=>.
TODO: Make use of js-classes.
*/

console.log("Tabel was loaded");

// remember last ordering so we can reverse order on second click.
let lastOrderedBy = null;
const reverseOrder = (o) => { return o === 'asc' ? 'desc' : 'asc'; }


// getter given type
const typeGetter = {
    boolean : (cell) => cell.children.length > 0 ? true : false, // FIXME hacky?
    string  : (cell) => cell.innerText,
}

// compare given type -- [GE : 1, EQ : 0, LE : -1]
const typeCompare = {
    boolean : (a, b) => (a > b ? 1 : a === b ? 0 : -1),
    string  : (a, b) => (a.localeCompare(b, 'en', {sensitivity: 'base'})),
}


// tabel tables
const Tabel = {};
Tabel.tables = [...document.getElementsByClassName("tabel")];
for (let table of Tabel.tables) { //FIXME is for-of supported?
  table.rowArray = [...table.rows];
  table.headers = [...table.rowArray.shift().cells]; // shift pops first  element (header)
  table.tbody = table.getElementsByTagName('tbody')[0];
}


// splits "a:asc,b:desc,c:desc" into [["a", "b", "c"], ["asc", "desc", "desc"]]
const splitter = (s) => {
    const [keys, orderings] = s
        .split(',') // splits on key:order,key:order pairs
        .map((s) => s.split(':')) // splits on key:order pars
        .reduce((prev, next) => next.map((item, i) => (prev[i] || []).concat(next[i])), []); // transpose (FIXME simplify?)

    return [keys, orderings]
}

// columns
for (let table of Tabel.tables) {
  table.columns = {};
  table.headers.map(
      (e, i) => {
          table.columns[e.dataset.headerId] = {
              header : e,                          // header html element
              type   : e.dataset.type,             // data type
              getter : typeGetter[e.dataset.type], // value of cell element
              sortBy : splitter(e.dataset.sortBy), // [keys, orderings]
              index  : i,                          // column index
          }
      }
  );
}

// get cell value
const getValue = (table, key, row) => {
    // get column given key
    const column = table.columns[`tabel-${key}`];

    // get cell given column index
    const cell = row.cells[column.index];

    // get value of cell
    let value = column.getter(cell);

    return value;
}

// compare value arrays (returns true if swap is needed)
const arrayCompare = (a, b, orderings) => {
    for (let i = 0; i < a.length; i++) {
        // get compare function given type
        const compare = typeCompare[typeof(a[i])];

        // compare depending on ascending or descending order
        const s = orderings[i] === 'asc' ?
            compare(a[i], b[i]) : compare(b[i], a[i]);

        switch (s) {
          case  1 : return true;  // swap
          case  0 : continue;     // inconclusive, check next element
          case -1 : return false; // no swap
        }
    }

    return false; // defaults to false when equal (no swap)
}

// sort table when clicking on header
Tabel.sort = function(table, e) {
    const headerId = e.currentTarget.dataset.headerId;
    const [keys, orderings] = table.columns[headerId].sortBy;

    // reverse ordering on toggle
    if (lastOrderedBy === keys[0]) {
        orderings[0] = reverseOrder(orderings[0]);

    }

    // bubble sort
    for (let i = table.rowArray.length; i > 0; i--) {
        for (let j = 0; j < i-1; j++) {
            const currentValue = keys.map((key) => getValue(table, key, table.rowArray[j]));
            const nextValue = keys.map((key) => getValue(table, key, table.rowArray[j+1]));

            const swap = arrayCompare(currentValue, nextValue, orderings);

            // swap rows
            if (swap) {
                const temp = table.rowArray[j];
                table.rowArray[j] = table.rowArray[j+1];
                table.rowArray[j+1] = temp;
            }
        }
    }

    // reset ordering if reversed, otherwise remember lastOrderedBy
    if (lastOrderedBy === keys[0]) {
        orderings[0] = reverseOrder(orderings[0]);
        lastOrderedBy = null;
    } else {
        lastOrderedBy = keys[0];
    }

    // update table (appendChild moves existing elements)
    for (let row of table.rowArray) {
        table.tbody.appendChild(row);
    }
}

// add onclick function to headers
for (let table of Tabel.tables) {
  for (let headerId in table.columns) {
      table.columns[headerId].header.onclick = (e) => Tabel.sort(table, e);

      // bootstrap glyphicon icons
      const icon = document.createElement('i');
      icon.classList.add("glyphicon", "glyphicon-sort");
      // glyphicon-sort-by-#
      table.columns[headerId].header.appendChild(icon);
  }
}
