// Using puppeteer for web scraping the img src from tripadvisor

const fs = require('fs');
const puppeteer = require('puppeteer');
const readline = require('readline');
const waittime = 7000;

// Read the sight urls from txt file into a dictionary
function geturl(){
  let dict = {};
  const rl = readline.createInterface({
    input: fs.createReadStream('testdata.txt')
  });

  rl.on('line', function (line) {
    var arr = line.split(",");
    dict[arr[0]] = arr[1];
  });
  return dict;
};

var dict = geturl();

// // print the dictionary
// function printurl(){
//   console.log('in print function');
//   console.log(dict);
// }

// set Timou out to make sure the geturl function is executed before the printurl function
// setTimeout(printurl,1000);

// read the sight urls from the dictionary, and pass them to the spider function
// The error file stores all the failures, most of them are page errors, such as can not find the selector, because the web page does not load completely.
// The result file stores the image urls accord to the sight 
async function getimg(){
  fs.appendFile('error.text', '====== new iteration =====' + '\n',function(err){});
  fs.appendFile('results.txt', '====== new iteration ====='+ '\n',function(err){});
  fs.appendFile('nophoto.txt', '====== new iteration ====='+ '\n',function(err){});
  for(var key in dict){
    console.log(key);
    await spider(key, dict[key]);
  }
}

setTimeout(getimg,2000);

async function findphoto(page,sight, sighturl){
  const fullviewselector = '#taplc_location_detail_above_the_fold_attractions_0 > div > div.row-reverse-contents.ui_columns.is-mobile > div.ui_column.is-8 > div > div > div.primaryWrap > div > div > div.carousel_images > div.entry_cta_wrap > span > span';
  const galleryselector = '#taplc_pv_resp_content_hero_zepto_0 > div > div.heroPhoto.photoRegion > div.prw_rup.prw_photoviewer_back_to_gallery > div > span';
  const gridclass = 'fillSquare';

  try {
    await page.click(fullviewselector);
    await page.waitFor(waittime);
    
    await page.click(galleryselector);
    await page.waitFor(waittime);
  }catch(e) {
    console.log('selector error');
    fs.appendFile('error.text', sight + ',' + sighturl + '\n', function(err){
      if (err) throw err;
    }); 
  }

  let imgs = await page.evaluate((sel) => {
    var divs = document.getElementsByClassName(sel);
    var imgsrcs = [];
    var i;
    for (i=0; i<divs.length; i++){
      if (divs[i].getElementsByTagName('img')[0].getAttribute('src') != null ){
        imgsrcs.push(divs[i].getElementsByTagName('img')[0].getAttribute('src'));
      }    
    }
    return imgsrcs;
  },gridclass);

  console.log(sight + '====length====' + imgs.length);
  fs.appendFile('results.txt', sight + '\n' + imgs.join('\n') + '\n', function(err){
    if (err) throw err;
  });
}

// Function spider takes the sight name and the sight url as the arguments.
// By using the puppeteer API, we can cread a brwoser page, and click according selectors to navigate to the gallery page which we want to web crawler.
// selector 预先设定好
// setViewport 设定了窗口的大小，从而也决定了载入的照片数量
async function spider(sight, sighturl){

  const browser = await puppeteer.launch({
  	headless: false
  });

  const page = await browser.newPage();
  page.setViewport({ width: 1280, height: 1800 });

  try {
    await page.goto(sighturl);
    await page.waitFor(waittime);
  }
  catch(e){
    console.log('goto error');
    fs.appendFile('error.text', sight + ',' + sighturl + '\n', function(err){
      if (err) throw err;
    }); 
  }

    let check = 'cta-text';
    //check if there is any photos
    var nullcheck = await page.evaluate((str) => {
      let ncheck = document.getElementsByClassName(str);
      return ncheck.length;
    },check);

    // There is no photos, apeend nophotofile
    if(nullcheck != 0){
      console.log('no photos');
      fs.appendFile('nophoto.txt', sight + ',' + sighturl + '\n', function(err){
        if (err) throw err;
      }); 
    }else{
      // There are photos
      await findphoto(page,sight, sighturl);
    }
  await browser.close();
}