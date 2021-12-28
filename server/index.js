const express = require("express");
const { MongoClient } = require('mongodb')

const PORT = process.env.PORT || 3001;
const URI = 'mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false';

const app = express();
const client = new MongoClient(URI);


app.listen(PORT, () => {
    console.log(`Server listening on ${PORT}`);
});

/**
 * Gets a word and search for it in the words db table.
 * 
 * @param {string} req.word - the word to look for.
 * @returns object that stores the name of the movie and the time where the word appeared.
 */
app.get('/words', async (req, res) => {
    const word = req.query.word;

    try {
        await client.connect();
        const database = client.db("infomotion");
        const words = database.collection("words");
        const json = await words.find({'name': word}).toArray();

        res.json(json);
    } finally {
        await client.close();
    }
});