"""
Testing strategies:
1. Functional testing
   a. Positive workflow : Verify functionality with positive wokflow
	 b. Negative workflow: Verify functionality with positive wokflow
	 c. Input validation : Verifing input parameters values, incorrect values.
	 d. Boundry validation : Verify functionality with incorrect boundry values.
	 e. Error messages : Veify user frinedly error messages for all errors.
2.  Scalaibility testing and Performance testing:
	Verify concurrent execution of API workflow to understand what is the scalability and peformance of the API.
3. Localization testing:
	Verify API behaviour with locale parameter
4. Regional Load Balancing testing
5. Security testing:
	a. Authentication, Authorization (If applicable as I didnt find any authorization support in Vonage.)
	b. SQL injections
	c. Denial of service attack - If huge no. of requests are coming with invalid JWT header
	
Test flows:
1. Testing API isolated : Testing one operation of the API in isolated mode
2. Testing multiple API operations: Testing multiple API operations, eg POST, GET, PUT and DELETE.

Above all testing can be done on all APIs, but as Conversation object is connected with the user, memeber, leg objects, hence I'm picking up Conversation API for testing.

TestCases for ConversationAPI module::
1. List all conversation
2. Create a conversation
	a. Create a conversation with all valid parameteres
	b. Create a conversation with an existing name, other valid parameters -  fail
	c. Create a conversation with an existing image, other valid parameters - Pass
3. Retrive a specific conversation
4. Edit a conversation
5. Delete a conversation
6. Record a conversation
"""

#Todo : Chatname is hardcoded need to generate it randomly 
#Todo : Auth key is hardcoded need to work on that

import requests
import json

#variable for Authentication Header
authHeader = {'Authorization' : 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE2MzUwNjc2NzMsImV4cCI6MTYzNTA4OTI3MywianRpIjoiZlkxNlZ3QWMzT044IiwiYXBwbGljYXRpb25faWQiOiIwMjYzYmViYS02MWU3LTQwZGQtODE1OC0yZmY1ZmY3ZDU5MjEifQ.mVLTMgSRDvwRJhMOZdyv6ZZNCs-VPpkAV2QSxyhGR__gjVMC2Ocq1qO9YzTHJH-v441dnnBiXJ9OvDYVSNzSWbVJzhRiuv1ibjibTAKzN7GQQ-z0chcS-LePUFHWr6jlZfPzU0F0k79yRCsjIAsnzHvLvGd_wAxOvY6rgUqwJ9MZ5lGEk5hBIB9SFU8Iq-UtbL96fw6eFxSaPyHXL-iOaCZIJxNbV7SJ0E1gjgvq6HfmtpVBb58nRjLuEhRO2f1XdDi9INMiQt0l3y9fWFwoBR7Vk_GnFFGgiXbabI0EIu2FRgATECT2j6zh3FK6oLdwO85a-7JzXGbtAyb02avbpQ'}

#variable for Conversation API
conversationAPI = 'https://api.nexmo.com/v0.1/conversations'

# list conversations
def getConveration(conversationId=''):
    print("Info: Inside getConveration ")
    targetAPI = conversationAPI
    if conversationId != '' :
        targetAPI = targetAPI+"/"+conversationId
    print("Info: TargetAPI value is: ", targetAPI)
    response = requests.get(targetAPI, headers=authHeader)
    if (response.status_code == 200):
        print("Info: Get operation successful. Returned object is:  ",response.json())
        return response, 0
    else:
        print("Error: Get operation failed. Error is : ", response)
        return response, 1


#Create conversation using Post method
def createConversation(param):
    print("Info: Inside updateConversationion ")
    print("Info: Input paramater: ", param)
    response = requests.post(conversationAPI,headers=authHeader,json = param)
    if ( response.status_code == 200):
        print("Info: Post operation successful. Returned object is:  ",response.json())
        return response, 0
    else:
        print("Error: Post operation failed. Error is : ", response.json())
        return response, 1


#update conversation : incomplete not tested
def updateConversation(conversationId):
    print("Info: Inside updateConversationion ")
    targetAPI = conversationAPI
    if conversationId != '':
        targetAPI = targetAPI + "/" + conversationId
    print("Info: TargetAPI value is: ",targetAPI)
    response = requests.put(targetAPI, headers=authHeader)
    if ( response.status_code == 200):
        print("Info: Put operation successful. Returned object is:  ",response.json())
        return response,0
    else:
        print("Error: Put operation failed. Error is : ", response)
        return response,1

#delete conversation
def deleteConversation(conversationId):
    print("Info: Inside deleteConversation ")
    targetAPI = conversationAPI
    if conversationId != '':
        targetAPI = targetAPI + "/" + conversationId
    print("Info: TargetAPI value is: ",targetAPI)
    response = requests.delete(targetAPI,headers=authHeader)
    if ( response.status_code == 200):
        print("Info: delete operation successful. Returned object is:  ",response.json())
        return 0
    else:
        print("Error: delete operation failed. Error is : ", response.json())
        return 1


#response = requests.get('https://api.nexmo.com/v0.1/conversations', headers=my_headers)
#print("Response is: ",response)

#Test to verify create conversation
def testCreateConversation():
    print("Info: Inside testCreateConversation ")
    conversationResponse, postResult = createConversation({"name": "chat_1","display_name": "Chat","image_url": "","properties": {"ttl": 60}})
    if postResult == 0:
        print("created JSON ",conversationResponse.json())
        print("Info: Conversationid:", conversationResponse.json()["id"])
        retResponse, getResult = getConveration(conversationResponse.json()["id"])
        if getResult == 0:
            print("Info: testCreateConversation Passed")
        else:
            print("Error: testCreateConversation failed, could not get create object")
    else:
        print("Error:testCreateConversation failed, could not create object")
        return 1



#This test verify the a conversation with the existing name fails.
#This function is to validate conversation with a same name does not get created.
def testCreateConversationWithExistingName():
    print("Info: Inside function testCreateConversationWithExistingName")
    conversationResponse, result = createConversation({"name": "1_chat_1", "display_name": "1_Chat_1", "image_url": "","properties": {"ttl": 60}})
    if result == 0:
        #print("Info: Created conversation succefully :", conversationResponse.json())
        conversationResponse, result = createConversation({"name": "1_chat_1", "display_name": "1_Chat_1", "image_url": "","properties": {"ttl": 60}})
        if conversationResponse.status_code != 200 :
            print("Info: Create conversation failed as expected:", conversationResponse.json())
            print("Info: testCreateConversationWithExistingName Passed")
        else:
            print("testCreateConversationWithExistingName Failed. Return status of duplicate object creation is ",conversationResponse.status_code)
    else:
        print("Error: testCreateConversationWithExistingName failed, could not create first object")
        return 1

#def testDeleteConversation():

def main():
    print("Info: Inside main")
    testCreateConversation()
    testCreateConversationWithExistingName()


if __name__=="__main__":
    main()

