import json
import boto3

dynamodb = boto3.resource('dynamodb')
fiek_students_table = dynamodb.Table('fiek_students')
fiek_departments_table = dynamodb.Table('fiek_departments')

def lambda_handler(event, context):
    try:
        path = event['requestContext']['http']['path']
        body = json.loads(event['body'])
        
        if path == '/students':
            # Get user data from the request body
            student_id = body.get('student_id')
            username = body.get('username')
            department_id = body.get('department_id')
            
            # Check if the department exists
            department_response = fiek_departments_table.get_item(
                Key={
                    'department_id': department_id
                }
            )
            
            if 'Item' not in department_response:
                # Department does not exist
                response = {
                    'statusCode': 404,
                    'body': json.dumps('Department with the specified ID does not exist')
                }
            else:
                # Department exists, save the user
                fiek_students_table.put_item(
                    Item={
                        'student_id': student_id,
                        'username': username,
                        'department_id': department_id
                    }
                )
                
                response = {
                    'statusCode': 200,
                    'body': json.dumps('User created successfully')
                }
            
        elif path == '/departments':
            # Create a department
            department_id = body.get('department_id')
            department_name = body.get('department_name')
            
            fiek_departments_table.put_item(
                Item={
                    'department_id': department_id,
                    'department_name': department_name
                }
            )
            
            response = {
                'statusCode': 200,
                'body': json.dumps('Department created successfully')
            }
            
        else:
            response = {
                'statusCode': 404,
                'body': json.dumps('Invalid path')
            }
    except Exception as e:
        response = {
            'statusCode': 500,  # Internal Server Error
            'body': json.dumps('Something went wrong. Try again later')
        }
    
    return response
