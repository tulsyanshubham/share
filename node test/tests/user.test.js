// https://github.com/chaijs/chai/issues/1578

import { app, server } from "../server.js";
// import { connect, connection } from "mongoose";
import pkg from 'mongoose';
const { connect, connection } = pkg;
import { v4 as uuidv4 } from 'uuid';

import chaiHttp from "chai-http";
import * as chai from "chai";
const should = chai.should();
const expect = chai.expect;

const request = chai.use(chaiHttp).request.execute;

// use(chaiHttp);
// const { expect } = chai;
const testDbName = `testdb_${uuidv4()}`;

describe("User API", () => {
    // Before running tests, connect to the database
    before(async () => {
        await connect(`mongodb://127.0.0.1:27017/${testDbName}`);
    });

    // After tests, disconnect from the database
    after(async () => {
        await connection.db.dropDatabase(); 
        await connection.close();
        server.close();
    });

    let userId;

    // Test: Create User
    it("should create a new user", (done) => {
        request(app)
            .post("/users")
            .send({ name: "John Doe", email: "john@example.com" })
            .end((err, res) => {
                expect(res).to.have.status(201);
                expect(res.body).to.have.property("_id");
                expect(res.body.name).to.equal("John Doe");
                userId = res.body._id; // Store ID for future tests
                done();
            });
    });

    // Test: Get All Users
    it("should retrieve all users", (done) => {
        request(app)
            .get("/users")
            .end((err, res) => {
                expect(res).to.have.status(200);
                expect(res.body).to.be.an("array");
                done();
            });
    });

    // Test: Get User by ID
    it("should retrieve a user by ID", (done) => {
        request(app)
            .get(`/users/${userId}`)
            .end((err, res) => {
                expect(res).to.have.status(200);
                expect(res.body).to.have.property("_id", userId);
                done();
            });
    });

    // Test: Update User
    it("should update a user", (done) => {
        request(app)
            .put(`/users/${userId}`)
            .send({ name: "John Updated" })
            .end((err, res) => {
                expect(res).to.have.status(200);
                expect(res.body.name).to.equal("John Updated");
                done();
            });
    });

    // Test: Delete User
    it("should delete a user", (done) => {
        request(app)
            .delete(`/users/${userId}`)
            .end((err, res) => {
                expect(res).to.have.status(200);
                expect(res.body).to.have.property("message", "User deleted successfully");
                done();
            });
    });
});
