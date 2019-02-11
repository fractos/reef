# reef

Retrieve top ten latest Google searches for a query as an RSS or ATOM feed.

Can place output XML in either a folder or an S3 bucket (and optionally setting it to public-read ACL).

## Environment variables

| Name              | Description                                           | Default |
|-------------------|-------------------------------------------------------|---------|
| DEBUG             | Enable debug output in log                            | False   |
| SLEEP_SECONDS     | Number of seconds to sleep between runs               | 60      |
| MAX_WORKERS       | Maximum number of concurrent workers                  | 2       |
| DB_TYPE           | Database type (sqlite or postgresql)                  | sqlite  |
| CONFIG_FILE       | (optional) file containing queries to add             |         |
| BASE_URL          | (required) Base URL of RSS output                     |         |
| FEED_FORMAT       | Feed format to output as (rss or atom)                | rss     |
| RESULTS_FOLDER    | URI of place to save RSS feed XML (path or S3:// URI) |         |
| S3_SET_PUBLIC_ACL | Set the S3 object for feed XML as public-read ACL     | False   |
| DB_NAME           | sqlite: path of db file, postgresql: database name    | reef.db |
| DB_HOST           | postgresql: hostname of database server               |         |
| DB_USER           | postgresql: username to login as                      |         |
| DB_PASSWORD       | postgresql: password for login                        |         |

## aws policy for user/task

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:DeleteObject",
        "s3:GetObject",
        "s3:GetObjectAcl",
        "s3:ListBucket",
        "s3:PutObject",
        "s3:PutObjectAcl"
      ],
      "Resource": [
        "<bucket ARN>",
        "<bucket ARN>/*"
      ]
    }
  ]
}
```

## config file format

```
{
  "queries": [
    {
      "id": "query-1",
      "search": "adam christie fractos"
    }
  ]
}
```
