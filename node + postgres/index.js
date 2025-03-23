require('dotenv').config();
const express = require('express');
const { Pool } = require('pg');

const app = express();
const port = 3000;

// PostgreSQL connection
const pool = new Pool({
    user: process.env.DB_USER,
    host: process.env.DB_HOST,
    database: process.env.DB_NAME,
    password: process.env.DB_PASSWORD,
    port: process.env.DB_PORT,
});

app.use(express.json());

// Create a student
app.post('/students', async (req, res) => {
    const { name, age, email } = req.body;
    try {
        const result = await pool.query(
            'INSERT INTO students (name, age, email) VALUES ($1, $2, $3) RETURNING *',
            [name, age, email]
        );
        res.status(201).json(result.rows[0]);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Get all students
app.get('/students', async (req, res) => {
    try {
        const result = await pool.query('SELECT * FROM students');
        res.json(result.rows);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Get a student by ID
app.get('/students/:id', async (req, res) => {
    const { id } = req.params;
    try {
        const result = await pool.query('SELECT * FROM students WHERE id = $1', [id]);
        if (result.rows.length === 0) return res.status(404).json({ error: 'Student not found' });
        res.json(result.rows[0]);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Update a student
app.put('/students/:id', async (req, res) => {
    const { id } = req.params;
    const { name, age, email } = req.body;
    try {
        const result = await pool.query(
            'UPDATE students SET name = $1, age = $2, email = $3 WHERE id = $4 RETURNING *',
            [name, age, email, id]
        );
        if (result.rows.length === 0) return res.status(404).json({ error: 'Student not found' });
        res.json(result.rows[0]);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

// Delete a student
app.delete('/students/:id', async (req, res) => {
    const { id } = req.params;
    try {
        const result = await pool.query('DELETE FROM students WHERE id = $1 RETURNING *', [id]);
        if (result.rows.length === 0) return res.status(404).json({ error: 'Student not found' });
        res.json({ message: 'Student deleted' });
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});
