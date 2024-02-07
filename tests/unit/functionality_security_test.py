import json
import requests
import pytest

# This sample event and context can be used to test lambda functionality

event_get = {
    "version": "2.0",
    "routeKey": "$default",
    "rawPath": "/dev/test/visits",
    "rawQueryString": "",
    "headers": {
        "content-length": "0",
        "host": "api.oderalabs.link",
        "user-agent": "Amazon CloudFront",
        "via": "1.1 XXXXXXXXXX.cloudfront.net (CloudFront)",
        "x-amz-cf-id": "XXXXXXXXXXXXXXXXXX",
        "x-amzn-trace-id": "Root=1-65ae0723-569924ba0b375f371537c21d",
        "x-forwarded-for": "xx.xx.xx.xx, xx.xx.xx.xx",
        "x-forwarded-port": "443",
        "x-forwarded-proto": "https"
    },
    "requestContext": {
        "accountId": "XXXXXXXXXXXX",
        "apiId": "XXXXXXXX",
        "domainName": "api.oderalabs.link",
        "domainPrefix": "api",
        "http": {
            "method": "GET",
            "path": "/dev/test/visits",
            "protocol": "HTTP/1.1",
            "sourceIp": "XX.XX.XX.XX",
            "userAgent": "Amazon CloudFront"
        },
        "requestId": "R7YNjg0iIAMEMlw=",
        "routeKey": "$default",
        "stage": "dev",
        "time": "22/Jan/2024:06:11:47 +0000",
        "timeEpoch": 1705903907216
    },
    "stageVariables": {
        "lambdaAlias": "dev"
    },
    "isBase64Encoded": False
}

event_options = {
    "version": "2.0",
    "routeKey": "$default",
    "rawPath": "/dev/test/visits",
    "rawQueryString": "",
    "headers": {
        "content-length": "0",
        "host": "api.oderalabs.link",
        "user-agent": "Amazon CloudFront",
        "via": "1.1 XXXXXXXXXX.cloudfront.net (CloudFront)",
        "x-amz-cf-id": "T-jblVWNUyJJr2j-EqnjOMe1LdIDVb4QsLvtYvgdkqaCR32cn0Q4fg==",
        "x-amzn-trace-id": "Root=1-65ae1878-0212a93b011558072615349b",
        "x-forwarded-for": "xx.xx.xx.xx, xx.xx.xx.xx",
        "x-forwarded-port": "443",
        "x-forwarded-proto": "https"
    },
    "requestContext": {
        "accountId": "XXXXXXXXXXXX",
        "apiId": "XXXXXXXX",
        "domainName": "api.oderalabs.link",
        "domainPrefix": "api",
        "http": {
            "method": "OPTIONS",
            "path": "/dev/test/visits",
            "protocol": "HTTP/1.1",
            "sourceIp": "XX.XX.XX.XX",
            "userAgent": "Amazon CloudFront"
        },
        "requestId": "R7jCzjtqoAMEV2w=",
        "routeKey": "$default",
        "stage": "dev",
        "time": "22/Jan/2024:07:25:44 +0000",
        "timeEpoch": 1705908344044
    },
    "stageVariables": {
        "lambdaAlias": "dev"
    },
    "isBase64Encoded": False
}

context = "LambdaContext([aws_request_id=5f477f94-0c22-4a81-9abf-087f095edeb4,log_group_name=Lambda_logs_cresume,log_stream_name=2024/01/22/DynamodbLambdaAPIGatewayS-VisitorCountLambda[$LATEST]09135717237a403f818b05452c87e9a2,function_name=DynamodbLambdaAPIGatewayS-VisitorCountLambda,memory_limit_in_mb=128,function_version=$LATEST,invoked_function_arn=arn:aws:lambda:region:account:function:DynamodbLambdaAPIGatewayS-VisitorCountLambda7AA70C-zmsAGjUTvOzN:dev,client_context=None,identity=CognitoIdentity([cognito_identity_id=None,cognito_identity_pool_id=None])])"

class FunctionalityTests:
    '''Class for testing the functionality of the website and api'''
    
    
    def webpage_test(endpoint: str, headers: dict, verify: bool) -> requests.Response:
        '''Test the webpage for successful functionality - returning 200 OK'''
        print(f"Testing the webpage at {endpoint}\n")
        response = requests.get(endpoint, headers=headers, verify=verify)
        assert response.status_code == 200, f"Error: {response.text}"
        print(f"Success! The webpage loaded with status code : {response.status_code}\n")
    

    def api_test_GET(endpoint: str, headers: dict, verify: bool) -> requests.Response:
        '''Test the API for successful functionality - returning visitor count'''
        print(f"Testing the api at {endpoint}\n")
        response = requests.get(endpoint, headers=headers, verify=verify)
        assert response.status_code == 200, f"Error: {response.text}"
        # verify the response from the api can be turned into an int (is a number)
        assert isinstance(int(response.text), int) 
        print(f"Success! The api responded with the visitor count: {response.text}\n")
    

    def api_test_OPTIONS(endpoint: str, headers: dict, verify: bool) -> requests.Response:
        '''Test the API for successful functionality - returning cors pre-flight options'''
        print(f"Testing the api at {endpoint} for cors pre-flight options\n")
        ## get the cors pre-flight options from the api and assert that the api responds with 200OK and the cors pre-flight options are returned
        ## note that the api responds with the cors pre-flight options even if the request is a GET request, so we need to test the OPTIONS method separately
        response = requests.options(endpoint, headers=headers, verify=verify)
        assert response.status_code == 200, f"Error: {response.text}"
        assert response.headers["Access-Control-Allow-Methods"] == "GET, OPTIONS"
        assert response.headers["Access-Control-Allow-Headers"] == "*"
        assert response.headers["Access-Control-Allow-Origin"] == "h*"
        print(f"Success! The api responded with the cors pre-flight options:\n {json.dumps(dict(response.headers), indent=4)}\n")

    def api_test_incrementation(endpoint: str, headers: dict, verify: bool = True) -> requests.Response:
        '''Test the API for successful functionality - incrementing the visitor count'''
        print(f"Testing the api at {endpoint} for incrementing the visitor count\n")    
        ## get the visitor count twice and assert that the count is incremented by one
        response = requests.get(endpoint, headers=headers, verify=verify)
        count1 = int(response.text)
        response = requests.get(endpoint, headers=headers, verify=verify)
        count2 = int(response.text)
        assert count2 == count1 + 1, f"Error: {response.text}"
        print(f"Success! The API incremented the counter from: {count1} to {count2}\n")
    
class SecurityTests:
    '''Class for testing the security of the website and api'''   

    def webpage_redirect_test(endpoint: str, headers: dict, verify: bool) -> requests.Response:
        '''Test the webpage for successfully redirecting any http to https'''
        print(f"Testing the api at {endpoint} for security\n")    
        ## Ensure that webpage requests are redirected to https
        response = requests.get(endpoint, headers=headers, verify=verify)
        assert response.history[0].status_code == 301 , f"Error: {response.text}"
        print(f"Success! The API redirected to https\n")
    
    def strict_transport_test(endpoint: str, headers: dict, verify: bool) -> requests.Response:
        '''Test the API to ensure that it rejects http connections'''
        print(f"Attempting to access the api at {endpoint}, testing for strict transport security\n")    
        ## Ensure that the api rejects requests that are not https and http is redirected to https on the webpage
        response = requests.get(endpoint, headers=headers, verify=verify)
        response_status = response.status_code
        assert response.status_code == 404 or response.status_code == 403, f"Error: {response.text}"
        response = requests.options(endpoint, headers=headers, verify=verify)
        response_status2 = response.status_code
        assert response.status_code == 404 or response.status_code == 403, f"Error: {response.text}"
        print(f"Success! The API rejected GET and OPTIONS requests that were not https with {response_status} and {response_status2} code errors respectiviely\n")

def test_runner():
    '''Test the webpage for successful functionality - returning 200 OK'''
    webpage_url = "https://oderalabs.link/"
    http_webpage_url = "http://oderalabs.link/"
    api_page_url = "https://oderalabs.link/count/visits"
    http_api_url = "http://oderalabs.link/count/visits"
    headers = {"Content-Type": "application/json", "User-Agent":"vsCode", "Connection":"keep-alive"}
    FunctionalityTests.webpage_test(webpage_url, headers, verify=True)
    FunctionalityTests.api_test_GET(api_page_url, headers, verify=True)
    FunctionalityTests.api_test_OPTIONS(api_page_url, headers, verify=True)
    FunctionalityTests.api_test_incrementation(api_page_url, headers, verify=True)
    SecurityTests.webpage_redirect_test(http_webpage_url, headers, verify=True)
    SecurityTests.strict_transport_test(http_api_url, headers, verify=True)
    print("All tests passed!")
    






