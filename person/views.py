from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from bson import ObjectId
from .db_connection import mongo_db
from .serializers import MyApiSerializer

class MyApiView(APIView):
    @swagger_auto_schema(
        request_body=MyApiSerializer,
        responses={201: openapi.Response('Success', MyApiSerializer), 400: 'Validation Error'},
        operation_id='post_document',
        operation_description='Create a new document'
    )
    def post(self, request):
        serializer = MyApiSerializer(data=request.data)
        
        if serializer.is_valid():
            # Insert the document into the collection
            collection = mongo_db['test_collection']
            result = collection.insert_one(serializer.validated_data)
            
            # Retrieve the inserted document
            inserted_document = collection.find_one({"_id": result.inserted_id})
            if inserted_document:
                inserted_document['_id'] = str(inserted_document['_id'])  # Convert ObjectId to string
            
            # Prepare the response with the inserted document
            response_data = {
                "message": "Data inserted successfully",
                "inserted_document": inserted_document
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_id='get_all_documents',
        operation_description='Retrieve all documents',
        responses={200: openapi.Response('Success', openapi.Schema(
            type='array',
            items=openapi.Schema(
                type='object',
                properties={
                    'name': openapi.Schema(type='string'),
                    'age': openapi.Schema(type='integer'),
                    '_id': openapi.Schema(type='string')
                }
            )
        ))}
    )
    def get(self, request, id=None):
        collection = mongo_db['test_collection']
        
        if id:
            # Get a single document by ID
            document = collection.find_one({"_id": ObjectId(id)})
            if document:
                document['_id'] = str(document['_id'])
                return Response({"data": document})
            return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Get all documents
            data = collection.find()
            data_list = []
            for document in data:
                document['_id'] = str(document['_id'])  # Convert ObjectId to string
                data_list.append(document)
            return Response({"data": data_list})

    @swagger_auto_schema(
        request_body=MyApiSerializer,
        responses={200: openapi.Response('Success', MyApiSerializer), 404: 'Document not found', 400: 'Validation Error'},
        operation_id='put_document',
        operation_description='Update a document by ID',
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description='Document ID', type=openapi.TYPE_STRING, required=True)
        ]
    )
    def put(self, request, id=None):
        if not id:
            return Response({"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = MyApiSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            collection = mongo_db['test_collection']
            update_result = collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": serializer.validated_data}
            )
            if update_result.matched_count == 0:
                return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)
            
            updated_document = collection.find_one({"_id": ObjectId(id)})
            updated_document['_id'] = str(updated_document['_id'])
            return Response({
                "message": "Data updated successfully",
                "updated_document": updated_document
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={204: 'No Content', 404: 'Document not found'},
        operation_id='delete_document',
        operation_description='Delete a document by ID',
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description='Document ID', type=openapi.TYPE_STRING, required=True)
        ]
    )
    def delete(self, request, id=None):
        if not id:
            return Response({"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        collection = mongo_db['test_collection']
        delete_result = collection.delete_one({"_id": ObjectId(id)})
        
        if delete_result.deleted_count == 0:
            return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"message": "Data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
