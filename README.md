# url-lookup-service
Problem Statement:

We have an HTTP proxy that is scanning traffic looking for malware URL's. Before allowing HTTP connections to be made, this proxy asks a service that maintains several databases of malware URL's, if the resource being requested is known to contain malware.

We have to create a small web service, that responds to GET requests, where the caller passes in a URL and the service responds with some information about that URL.
The GET requests would look like this:

GET /urlinfo/1/{hostname_and_port}/{original_path_and_query_string}
