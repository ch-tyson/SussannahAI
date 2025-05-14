const cohere = require("cohere-ai");
const express = require("express");
const cors = require("cors");
require("dotenv").config();

const { writeToJson } = require("./utils");

const app = express();
app.use(cors());

app.use(express.json());

cohere.init(process.env.API_KEY);
