# AWS example

There is a Cloud service in AWS called [S3](https://aws.amazon.com/s3/) used for data storage.
Function under test here lists all files and directories in given path.
Just like [ls](https://www.geeksforgeeks.org/ls-command-in-linux/).

## Regular mock
no_di/test_with_generic_patch.py basically hardcodes response from a function produced with boto3.

It doesn't simulate any object storage, where we could put files.
If there are more methods of obtaining object list from S3,
that test won't be able to support it, because it mocks one specific method.

## Moto
no_di/test_with_moto.py prepares a simulation of S3 in local system memory.

It means that moto will dynamically respond to given ls path.
In other words, with moto you can get these responses:
```python
result = ls(".")
result == ["file1.txt", "sub/path/file2.txt"]
```
```python
result = ls("path/to/list")
result == ["sub/path/file2.txt"]
```
as opposed to the previous implementation, where ls response is static.

## Custom created object injection
with_di/test_with_custom_object.py is similar to Regular mock example.

The only difference is that it doesn't require monkey-patching to work.
This is also why the implementation looks simpler here.

## Localstack
with_di/test_with_localstack.py is a more complete approach, fitting more under the "integration tests" category.

Here we actually start a service on localhost, that simulates the behaviour of AWS S3.

Steps to set this test up (also you can refer to [this article](https://dev.to/r0mymendez/learning-aws-s3-on-localhost-best-practices-with-boto3-and-localstack-cmn)):
- Install and start [docker](https://www.docker.com/) env 
- Run this in any directory `git clone https://github.com/r0mymendez/LocalStack-boto3.git`
- `cd LocalStack-boto3`
- Run pytest and provide path to LocalStack-boto3: `pytest --docker-compose-path=C:/Path/To/LocalStack-boto3`

You could treat this solution as bringing moto to the next level.
moto prepares S3 object in system memory, while localstack is a different process exposing a real service on localhost.

This gives additional testing capabilities, as data flows via real network interfaces.
Also, using localstack in general is not python-bound.

Any programming language could utilize it for testing purposes.

## Comparison

|                             | Regular mock | Moto               | Custom object      | Localstack         |
|-----------------------------|--------------|--------------------|--------------------|--------------------|
| speed                       | very fast    | fast               | very fast          | :snail:            |
| no monkey-patching          | :x:          | :x:                | :white_check_mark: | :white_check_mark: |
| dynamic response            | :x:          | :white_check_mark: | :x:                | :white_check_mark: |
| lines of code to prepare S3 | ~14          | ~9                 | ~18                | ~30                |

## Personal opinion
Considering all the analysis above, I think that for this particular example:

moto > localstack > custom object > regular mock