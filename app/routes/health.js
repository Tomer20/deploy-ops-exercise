const Promise = require('bluebird');
const express = require('express');
const mongoose = require('mongoose');
const { exec } = require('child_process');

const router = express.Router();


function checkDatabase() {
  const Image = mongoose.model('Image')
  return Image.count();
}

function checkDisk() {
  return new Promise((resolve, reject) => {
    exec('ls /', (error, stdout, stderr) => {
      if (error) {
        reject(error);
      } else {
        resolve()
      }
    })
  })
}

function healthCheck() {
  const checks = [checkDatabase, checkDisk]
  return Promise.reduce(checks, (result, check) => {
    return check().then((checkResult) => {
      result[check.name] = {
        success: true,
        result: checkResult
      }
      return result;
    }, (error) => {
      result[check.name] = {
        success: false,
        result: error.message
      }
      result.isSuccessful = false
      return result;
    })
  }, { isSuccessful: true} )
}

/* GET home page. */
router.get('/', function(req, res, next) {
  healthCheck().then((result) => {
    const status = result.isSuccessful === false ? 500 : 200;
    res.status(status).send(result);
  }, (err) => {
    res.status(500).send( { isSuccessful: false, error: err.message});
  })

});

module.exports = router;
