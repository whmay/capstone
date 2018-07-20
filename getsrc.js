// Using puppeteer for web scraping the img src from tripadvisor
// sighturl 存在csv文件中
// selector 预先设定好
// setViewport 设定了窗口的大小，从而也决定了载入的照片数量
// 照片的url 存入csv文件中

// const sight = 'Hong_Kong-Hong Kong Skyline';
// const sighturl = 'https://www.tripadvisor.com/Attraction_Review-g294217-d2482919-Reviews-Hong_Kong_Skyline-Hong_Kong.html';
const fs = require('fs');
const puppeteer = require('puppeteer');

foo(process.argv[2],process.argv[3]);

function foo(sight, sighturl){
  spider(sight, sighturl);
}

async function spider(sight, sighturl){

  const browser = await puppeteer.launch({
  	headless: false
  });

  const page = await browser.newPage();
  page.setViewport({ width: 1280, height: 1800 });

  //const sight = './' + 'Hong_Kong/Hong Kong Skyline' +'.txt';
  //preprocess the sightname:change the slash to - in the sightname
  const filename = './' + sight +'.txt';
  // const sighturl = 'https://www.tripadvisor.com/Attraction_Review-g294217-d2482919-Reviews-Hong_Kong_Skyline-Hong_Kong.html';

  const fullviewselector = '#taplc_location_detail_above_the_fold_attractions_0 > div > div.row-reverse-contents.ui_columns.is-mobile > div.ui_column.is-8 > div > div > div.primaryWrap > div > div > div.carousel_images > div.entry_cta_wrap > span > span';
  const galleryselector = '#taplc_pv_resp_content_hero_zepto_0 > div > div.heroPhoto.photoRegion > div.prw_rup.prw_photoviewer_back_to_gallery > div > span';
  
  await page.goto(sighturl);
  await page.waitFor(1000);
  
  await page.click(fullviewselector);
  await page.waitFor(1000);
  
  await page.click(galleryselector);
  await page.waitFor(1000);

  const gridclass = 'fillSquare';
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

  console.log(imgs.length);
  fs.writeFileSync(filename, sight + '\n');
  fs.appendFile(filename, imgs.join('\n') + '\n');

  await browser.close();
}