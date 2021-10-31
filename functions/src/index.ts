import * as functions from "firebase-functions";
import * as admin from "firebase-admin";
import * as moment from "moment";
admin.initializeApp();

// Creates a new document for a specified id - contains an active field used to control storing of data
export const createNewProfileForComputerName = functions.https.onRequest(
  async (request, response) => {
    const firestore = admin.firestore();

    const requestBody: { id?: string } = JSON.parse(request.body);

    //Check Request is valid
    if (!requestBody.id) {
      response.sendStatus(400);
      return;
    }

    //create new document for a computer name
    await firestore
      .collection(collectionName)
      .doc(requestBody.id)
      .set({ active: false });

    // send good response
    response.sendStatus(200);
  }
);

// Returns false or true if data should be being stored
export const getShouldBeStoringKeyPressData = functions.https.onRequest(
  async (request, response) => {
    const firestore = admin.firestore();

    const requestBody: { id?: string } = JSON.parse(request.body);

    //Check Request is valid
    if (!requestBody.id) {
      response.sendStatus(400);
      return;
    }

    //fetch active attribute from document
    const doc = await firestore
      .collection(collectionName)
      .doc(requestBody.id)
      .get();

    // send good response
    response.status(200).send({ status: doc.get("active") });
  }
);

//sets the status of the computer to either true or false if we should be collecting data or not
//if we are turning it true, we are starting a new session so we need a new key press data array
export const setShouldBeStoringKeyPressData = functions.https.onRequest(
  async (request, response) => {
    const firestore = admin.firestore();

    const requestBody: { id?: string; newStatus?: boolean } = JSON.parse(
      request.body
    );

    //Check Request is valid
    if (!requestBody.id || requestBody.newStatus === undefined) {
      response.sendStatus(400);
      return;
    }

    if (requestBody.newStatus === true) {
      //setting it to active so create a new session
      const sessionStart = moment().toISOString();
      await firestore
        .collection(collectionName)
        .doc(requestBody.id)
        .update({
          active: requestBody.newStatus,
          activeSession: sessionStart,
          [`keypressData_${sessionStart}`]: [],
        });
    } else {
      //close the session
      await firestore
        .collection(collectionName)
        .doc(requestBody.id)
        .update({ active: requestBody.newStatus });
    }

    // send good response
    response.sendStatus(200);
  }
);

//stores keypress data on document
//expecting an array of key and timestamp values passed (object array)
//just merge it on active session keypress array
export const storeKeyPressDataForComputerName = functions.https.onRequest(
  async (request, response) => {
    const firestore = admin.firestore();

    const requestBody: { id?: string; newKeypressData?: any[] } = JSON.parse(
      request.body
    );

    //Check Request is valid
    if (!requestBody.id || requestBody.newKeypressData === undefined) {
      response.sendStatus(400);
      return;
    }

    //get active session
    const doc = await firestore
      .collection(collectionName)
      .doc(requestBody.id)
      .get();

    //update document with new data
    await firestore
      .collection(collectionName)
      .doc(requestBody.id)
      .update({
        [`keypressData_${doc.get("activeSession")}`]:
          admin.firestore.FieldValue.arrayUnion(...requestBody.newKeypressData),
      });

    // send good response
    response.sendStatus(200);
  }
);
