const image_input = document.getElementById("image_input");
var uploaded_image = "";
let x =0;
let m = 0;

let choiceMag1;



function ischecked(){
  if (document.getElementById("filter_flag").checked){
    document.getElementById("mess").textContent="Outer Cropping";
    $.ajax({
      type: "POST",
      url: "/upload/10",
      contentType: false,
      cache: false,
      processData: false,
      async: true,
      success: function (data) {
        document.getElementById("image_output").innerHTML= image_output();
  
      }})
  }

  else {
    document.getElementById("mess").textContent="Inner Cropping";
    $.ajax({
      type: "POST",
      url: "/upload/11",
      contentType: false,
      cache: false,
      processData: false,
      async: true,
      success: function (data) {
        document.getElementById("image_output").innerHTML= image_output();
  
      }})
  }
}

const toggleTo2 = document.getElementById("mag2_button");
const toggleTo1 = document.getElementById("mag1_button");

const hide = el => el.style.setProperty("display", "none");
const show = el => el.style.setProperty("display", "inline-block");

hide(toggleTo1);

toggleTo2.addEventListener("click", () => {
  hide(toggleTo2);
  show(toggleTo1);
});

toggleTo1.addEventListener("click", () => {
  hide(toggleTo1);
  show(toggleTo2);
});


function magfun1(){
  choiceMag1="0";
  images1();
  console.log("magnitude1 & phase2")
  $.ajax({
    type: "POST",
    url: "/upload/6",
    contentType: false,
    cache: false,
    processData: false,
    async: true,
    success: function (data) {
      document.getElementById("image_output").innerHTML= image_output();

    }})
}

function magfun2(){
  choiceMag1="1";
  images1();
  console.log("Magnitude2 & phase1")
  $.ajax({
    type: "POST",
    url: "/upload/3",
    // data: 1,
    contentType: false,
    cache: false,
    processData: false,
    async: true,
    success: function (data) {
      document.getElementById("image_output").innerHTML= image_output();

    }})

}

function images1(){
	var timestamp = new Date().getTime();    
	var sig = document.getElementById("signal"); 

  var timestamp2 = new Date().getTime();     
	var sig2 = document.getElementById("signal2"); 

  if (choiceMag1=="0"){ 
	sig.src = "/static/images/signal.jpg?t=" + timestamp; 
  console.log("e7na fe mag signal basss") 
  sig2.src = "/static/images/signalphase2.jpg?t=" + timestamp2; 
  console.log("e7na fe phase signal 2222222")
  }

  else if (choiceMag1=="1"){
    sig2.src = "/static/images/signal2.jpg?t=" + timestamp2;
    console.log("e7na fe mag signal 22222222222")
    sig.src = "/static/images/signalphase1.jpg?t=" + timestamp;
    console.log("e7na fe phase signal") 
  }  
	sig.classList.remove("hidden");

};

function image_output(){
  var timestamp = new Date().getTime();    
	var sig = document.getElementById("image_output"); 
  sig.src ="/static/images/combined.jpg?t=" + timestamp;
  sig.classList.remove("hidden");
}


image_input.addEventListener("change",function(){
    const reader = new FileReader();
    reader.addEventListener("load",() => {
        uploaded_image = reader.result;
        document.querySelector("#display_image").style.backgroundImage = `url(${uploaded_image})`; 
        choiceMag1="0";
        console.log("magnitude 1")
    })
    const form = document.getElementById("upload-image")
    reader.readAsDataURL(this.files[0]);
    const formData = new FormData(form)
    console.log(formData)
    $.ajax({
      type: "POST",
      url: "/upload/1",
      data: formData,
      contentType: false,
      cache: false,
      processData: false,
      async: true,
      success: function (data) {
        document.getElementById("signal").innerHTML= images1();
        document.getElementById("image_output").innerHTML= image_output();

      }})
})




const image_input2 = document.querySelector("#image_input2");
var uploaded_image2 = "";


image_input2.addEventListener("change",function(){
    const reader2 = new FileReader();
    reader2.addEventListener("load",() => {
        uploaded_image2 = reader2.result;
        document.querySelector("#display_image2").style.backgroundImage = `url(${uploaded_image2})`;
        choiceMag2="0";
        console.log("magnitude2")
    })
    const form = document.getElementById("upload-image2")

    reader2.readAsDataURL(this.files[0]);
    const formData = new FormData(form)
    $.ajax({
      type: "POST",
      url: "/upload/2",
      data: formData,
      contentType: false,
      cache: false,
      processData: false,
      async: true,
      success: function (data) {
        // console.log(form)
        document.getElementById("signal2").innerHTML= images1();
        document.getElementById("image_output").innerHTML= image_output();
        console.log("$$$$$$$$$")
      }})
})
/********************************************************Konva*************************************************************************/
var width = 270;
var height = 230;


var stage = new Konva.Stage({
  container: 'shape_container1',
  width: width,
  height: height,
});

var layer = new Konva.Layer();
let layer2 = new Konva.Layer();
let imageObj = new Image();
  imageObj.onload = function () {
      let yoda = new Konva.Image({
          x: 0,
          y: 0,
          image: imageObj,
          width: stage.width(),
          height: stage.height(),
      });
      // add the shape to the layer
      layer2.add(yoda);
  };


stage.add(layer);

stage.on("mousedown", function() { mousedownHandler(0); });
stage.on("mousemove", function() { mousemoveHandler(0); });
stage.on("mouseup", function() { mouseupHandler(0); });



let currentShape;
// setup menu
document.getElementById('Rect').addEventListener( "click" , function () {

  let item = new Konva.Rect({
    x: 80,
    y: 80,
    width: 100,
    height: 50,
    fill: 'ligthblue',
    opacity:0.4,
    draggable: true,
  });
  var tr = new Konva.Transformer();
  layer.add(tr);
  layer.add(item);
  tr.nodes([item]);
  x = tr;
  layer.draw();
});



var menuNode = document.getElementById('menu');
document.getElementById('delete-button').addEventListener('click', () => {
const tr = layer.find('Transformer').toArray().find(tr => tr.nodes()[0] === currentShape);
tr.destroy();
currentShape.destroy();
layer.draw();
});

  window.addEventListener('click', () => {
    // hide menu
    menuNode.style.display = 'none';
  });

  stage.on('contextmenu', function (e) {
    // prevent default behavior
    e.evt.preventDefault();
    if (e.target === stage) {
      // if we are on empty place of the stage we will do nothing
      return;
    }
    currentShape = e.target;
    console.log(currentShape);
    // show menu
    menuNode.style.display = 'initial';
    var containerRect = stage.container().getBoundingClientRect();
    menuNode.style.top =
      containerRect.top + stage.getPointerPosition().y + 4 + 'px';
    menuNode.style.left =
      containerRect.left + stage.getPointerPosition().x + 4 + 'px';
  });


/*********************************************************Shapes for the second canvas **********************************************************/ 
var stage1 = new Konva.Stage({
  container: 'shape_container2',
  width: width,
  height: height,
});

var layer1 = new Konva.Layer();
stage1.add(layer1);

stage1.on("mousedown", function() { mousedownHandler(1); });
stage1.on("mousemove", function() { mousemoveHandler(1); });
stage1.on("mouseup", function() { mouseupHandler(1); });


let currentShape1;
// setup menu
document.getElementById('Rect2').addEventListener( "click" , function () {

  let item1 = new Konva.Rect({
    x: 80,
    y: 80,
    width: 100,
    height: 50,
    fill: 'ligthblue',
    opacity:0.4,
    draggable: true,
  });
  var tr1 = new Konva.Transformer();
  layer1.add(tr1);
  layer1.add(item1);
  tr1.nodes([item1]);
  m = tr1;
  layer1.draw();

});
/****************************************************Delet menu to delet shapes**********************************************************/
var menuNode = document.getElementById('menu');
document.getElementById('delete-button').addEventListener('click', () => {
const tr1 = layer1.find('Transformer').toArray().find(tr1 => tr1.nodes()[0] === currentShape1);
tr1.destroy();
currentShape1.destroy();
layer1.draw();
});

  window.addEventListener('click', () => {
    // hide menu
    menuNode.style.display = 'none';
  });

  stage1.on('contextmenu', function (e) {
    // prevent default behavior
    e.evt.preventDefault();
    if (e.target === stage1) {
      // if we are on empty place of the stage we will do nothing
      return;
    }
    currentShape1 = e.target;
    console.log(currentShape1);
    // show menu
    menuNode.style.display = 'initial';
    var containerRect1 = stage1.container().getBoundingClientRect();
    menuNode.style.top =
      containerRect1.top + stage1.getPointerPosition().y + 4 + 'px';
    menuNode.style.left =
      containerRect1.left + stage1.getPointerPosition().x + 4 + 'px';
  });
/********************************************mouseup evnt**************************************************************/
function mousedownHandler(y) 
{

}

function mousemoveHandler(y)
{

}

function mouseupHandler(y)
{
    console.log(x.x());
    console.log(x.y());
    console.log(x.width());
    console.log(x.height());
    console.log(m.x());
    console.log(m.y());
    console.log(m.width());
    console.log(m.height());
    if (choiceMag1=="0"){
      $.ajax({
        type: "POST",
        url: 'http://127.0.0.1:5007/upload/4',
        contentType: "application/json; charset=utf-8",
        dataType: 'json',
        data: JSON.stringify({
                'x1':x.x(),
                'y1':x.y(),
                'w1':x.width(),
                'h1':x.height(),
                'x2':m.x(),
                'y2':m.y(),
                'w2':m.width(),
                'h2':m.height(),
              }),
              
 
        success: function (data) {
          console.log("mag1 pha2")
          document.getElementById("image_output").innerHTML= image_output();
        }})}

    else if (choiceMag1=="1")
      {
        $.ajax({
          type: "POST",
          url: 'http://127.0.0.1:5007/upload/5',
          contentType: "application/json; charset=utf-8",
          dataType: 'json',
          data: JSON.stringify({
                  'x1': x.x(),
                  'y1':x.y(),
                  'w1':x.width(),
                  'h1':x.height(),
                  'x2':m.x(),
                  'y2':m.y(),
                  'w2':m.width(),
                  'h2':m.height()
                }),
          
          success: function (data) {
            console.log("mag2 pha1")
            document.getElementById("image_output").innerHTML= image_output();
          }})
      }
    }
      

