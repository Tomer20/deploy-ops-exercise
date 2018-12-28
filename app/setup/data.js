const mongoose = require('mongoose');
const fs = require('fs');
const Promise = require('bluebird');
const retry = require('bluebird-retry');

const mongoUrl = "mongodb://panda:pow@db/pandaserve"

var connect = function() {
  return mongoose.connect(mongoUrl);
};

retry(connect, { max_tries: 15, interval: 1000 })
  .then(function(result) {
    console.log("Successfully connected to DB");
});

const Image = mongoose.model('Image', { filename: String });

console.log('Clearing historical images from MongoDB');
Image.remove({}).then(() => {
  const images = fs.readdirSync(`${__dirname}/../public/images`);

  console.log('Populating images in MongoDB');
  return Promise.all(images.map((image) => {
    const imageModel = new Image({ filename: image });
    imageModel.save();
  }))
})
