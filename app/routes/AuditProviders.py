from app.services.AuditService import AuditService
from app.services.TransactionService import TransactionService
from fastapi import APIRouter, HTTPException, Body
from app.services.RecoveryService import RecoveryService
from typing import List
import time
from app.config.firebaseConfig import db
import threading
router = APIRouter(
    prefix="/audit",
    tags=["audit"],
    responses={404: {"description": "Not found"}},
)


def count_documents(docs):
    counter = 0
    for doc in docs:
        counter += 1

    return counter


def build_response():
    docs = db.collection(u'Audit').stream()
    response = []
    for doc in docs:
        doc_dic = doc.to_dict()
        doc_dic["id"] = doc.id
        response.append(doc_dic)
    return response


@router.post("/")
async def begin_audit(params: dict = Body(...)):
    try:
        message = {
            "type": "audit",
            "parameters": params
        }
        auditor = AuditService()

        auditor.begin_audit(message)

        timeout = time.time() + 60 * 0.1  # 5 minutes from now
        # TODO: Crear parametros globales
        while count_documents(db.collection(u'Audit').stream()) != 10:
            print("Waiting for audit nodes.")
            time.sleep(1)
            if time.time() > timeout:
                break
        response = build_response()
        docs = db.collection(u'Audit').stream()
        for doc in docs:
            doc.reference.delete()
        return response
    except:
        return {"message": "There was a problem in the blockchain."}
