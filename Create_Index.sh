curl -XGET 'localhost:9200/pdf/_search?pretty' -H 'Content-Type: application/json' -d '
{
    "query" : {
       "query_string" : {
      "query" : "*Design*"
     
    }

    },

    }
}
'
