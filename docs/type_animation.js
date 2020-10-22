const elemIds = [
    {
        id: "slide-title1", 
        typed: false,
        cursor: false,
        timer: null,
        text: "",
        index: 0
    },
    {
        id: "slide-title2", 
        typed: false,
        cursor: false,
        timer: null,
        text: "",
        index: 0
    },
    {
        id: "slide-title3", 
        typed: false,
        cursor: false,
        timer: null,
        text: "",
        index: 0
    },
    {
        id: "slide-title4", 
        typed: false,
        cursor: false,
        timer: null,
        text: "",
        index: 0
    }
];
    
elemIds.forEach( (item, index) => {
    let e = document.getElementById(item.id);
    item.text = e.innerText.split("$")[1];
    e.innerText = "$";
});

var cursorVisible = false;
const typeDelay = 80;
const blinkInterval = 500;

document.onscroll = checkAnimations;            

function checkAnimations() {
    elemIds.forEach( (item, index) => {
        let e = document.getElementById(item.id);
        if(!item.typed && isVisible(e)) {
            item.typed = true;
            item.timer = setInterval(typeAnim, typeDelay, item);
        }
    });
}

function typeAnim(elemObj) {
    if(elemObj.index < elemObj.text.length) {
        document.getElementById(elemObj.id).innerHTML += elemObj.text.charAt(elemObj.index);
        elemObj.index++;
    } else {
        clearInterval(elemObj.timer);
        setInterval(blinkCursorElem, blinkInterval, elemObj);
    }
}

function blinkCursorElem(elemObj) {
    e = document.getElementById(elemObj.id);
    if(isVisible(e)) {
        if(elemObj.cursor) {
            t = e.innerHTML.slice(0, -1);
            e.innerHTML = t;
        } else {
            e.innerHTML += "_";
        }
        elemObj.cursor = !elemObj.cursor;
    }
}

function isVisible(e) {
    var bounding = e.getBoundingClientRect();
    return (
        bounding.top >= 0 &&
        bounding.left >= 0 &&
        bounding.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        bounding.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}
