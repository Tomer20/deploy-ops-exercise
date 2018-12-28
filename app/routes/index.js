const express = require('express');
const router = express.Router();
const fs = require('fs');
const mongoose = require('mongoose');

/* GET home page. */
router.get('/', function(req, res, next) {
  const Image = mongoose.model('Image')
  Image.find().select('filename').lean().then((images) => {
    res.render('index', { images: images || [] });
  })
});

module.exports = router;
