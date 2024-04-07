# AWS example

There is a Cloud service in AWS called [S3](https://aws.amazon.com/s3/) used for data storage.
Function under test here lists all files and directories in given S3 path.
Just like [ls](https://www.geeksforgeeks.org/ls-command-in-linux/) does in the unix file system.

## Regular mock
`no_di/test_with_generic_patch.py` basically hardcodes return value of a function from boto3.
It means that the tested function will have a static response.

This test doesn't simulate any object storage.

Furthermore, this test only mocks an explicit set of methods.
So if method for obtaining object list from S3 was replaced with a different one (with [list_objects](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/list_objects.html) for example),
this test wouldn't be able to support it.

## Moto
`no_di/test_with_moto.py` prepares a simulation of S3 in local system memory.

It means that moto will dynamically respond to given ls path.
With moto you can get different responses:
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
`with_di/test_with_custom_object.py` is similar to Regular mock example.

The only difference is that it doesn't require monkey-patching to work.
This is also why the implementation looks simpler here.

## Localstack
`with_di/test_with_localstack.py` is a more 'complete' approach, fitting more under the "integration tests" category.

Here we start a service on localhost, that simulates the behaviour of AWS S3.

Steps to set this test up (you can also refer to [this article](https://dev.to/r0mymendez/learning-aws-s3-on-localhost-best-practices-with-boto3-and-localstack-cmn)):
- Install and start [docker](https://www.docker.com/) env 
- Run this in any directory you want `git clone https://github.com/r0mymendez/LocalStack-boto3.git`
- `cd LocalStack-boto3`
- Run pytest and provide path to LocalStack-boto3: `pytest --docker-compose-path=C:/Path/To/LocalStack-boto3`

You could treat this solution as bringing moto to the next level.
moto prepares S3 object in system memory, while localstack is a separate process exposing S3 as http service.

This gives additional testing capabilities. Data flows via real network interfaces, so we can test timeouts, bad responses and resilliency more reliably.

Also, using localstack in general is not python-bound.
Many other programming languages could utilize it for testing purposes.

## Comparison table

|                             | Regular mock | Moto               | Custom object      | Localstack         |
|-----------------------------|--------------|--------------------|--------------------|--------------------|
| speed                       | very fast    | fast               | very fast          | :snail:            |
| no monkey-patching          | :x:          | :x:                | :white_check_mark: | :white_check_mark: |
| dynamic response            | :x:          | :white_check_mark: | :x:                | :white_check_mark: |
| lines of code to prepare S3 | ~14          | ~9                 | ~18                | ~30                |

## Final thoughts
Considering all things above, I think that for this particular example:

`moto > localstack > custom object > regular mock`

- Moto and localstack bring much better verification to the table
- Localstack is much more difficult to set up and is much slower
- Localstack doesn't seem to bring enough of additional testing value to justify time consumed by the tests and time consumed by test automation engineers to prepare those tests.

Still, in the end of the day, in a larger AWS project I would probably go with:
- moto in Unit Tests
- Localstack in Integration Tests
- AWS test cluster in System (E2E) Tests