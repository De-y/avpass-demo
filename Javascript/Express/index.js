const express = require('express');
const router = express.Router();
const request = require('request');
const { v4: uuidv4 } = require('uuid');
const { PrismaClient } = require('@prisma/client');
const crypto = require('crypto');
const prisma = new PrismaClient();
const client_id = process.env.client_id;
const client_secret = process.env.client_secret;

const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use('/', router);

router.get('/auth', async (req, res) => {
    const state = crypto.createHash('sha512').update(uuidv4()).digest('hex');
    await prisma.stateService.create({
      data: {
        ipAddress: req.ip,
        state: state
      }
    });
    const url = 'http://localhost:3000/oauth/initiate';
    const data = {
      state: state,
      client_id: client_id,
      client_secret: client_secret,
      redirect_uri: 'http://localhost/callback/avpass'
    };
    const response = await new Promise(resolve => {
      request.post({ url: url, json: data }, (error, response, body) => {
        if (error) throw new Error(error);
        resolve(response);
      });
    });
    const response_json = response.body;
    const uri = response_json.uri;
  
    res.redirect(uri);
  });
  
router.get('/avpass', async (req, res) => {
  const { code, state } = req.query;
  req.query.code = code;
  req.query.state = state;

  console.log(code)
  console.log(state)
  
  if (req.method === 'GET') {
    const tokenEndpoint = 'http://localhost:3000/oauth/api/user_info';
    const headers = { 'Content-Type': 'application/x-www-form-urlencoded' };
    const data = {
      client_id: client_id,
      client_secret: client_secret,
      auth_code: code
    };
    const response = await new Promise(resolve => {
      request.post({ url: tokenEndpoint, json: data }, (error, response, body) => {
        if (error) throw new Error(error);
        resolve(response);
      });
    });

    console.log(response.body)

    const stateValidator = await prisma.stateService.findFirst({
      where: {
        ipAddress: req.ip,
        state: state
      }
    });

    if (!stateValidator) {
      return res.status(403).json({ error: 'Invalid state' });
    }

    return res.send(`Your username is ${response.body.username}, your email is ${response.body.email}, and your email verification status is set to ${response.body.email_verified}.`);
  }
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`App listening on port ${PORT}`);
});
