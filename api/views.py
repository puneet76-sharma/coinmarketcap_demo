from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import psycopg2
from urllib.parse import urlencode
import requests
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .models import CoinMarket
from rest_framework.views import APIView
from .serializers import CoinSerializer

# Create your views here.

def bulkInsert(records):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="123456",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="coinmarket")
        cursor = connection.cursor()
        sql_insert_query = """ INSERT INTO api_coinmarket (name, price, one_hour, twenty_four_hour,
                        seven_days, market_cap, volume_24) VALUES (%s,%s,%s,%s,%s,%s,%s) """


        # executemany() to insert multiple rows
        result = cursor.executemany(sql_insert_query, records)
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into table")
        return((cursor.rowcount, "Record inserted successfully into table"))

    except (Exception, psycopg2.Error) as error:
        print("Failed inserting record into table {}".format(error))
        return("Failed inserting record into table {}".format(error))


    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


@csrf_exempt
def CoinApi(request,**args):
    if request.method=="POST":
        try:
            CoinMarket.objects.all().delete()
            print("deleting all rows")
        except Exception as e:
            print("error---",e)

        query_string = [
            ('start', '1'),
            ('limit', '100'),
            ('sortBy', 'market_cap'),
            ('sortType', 'desc'),
            ('convert', 'USD'),
            ('cryptoType', 'all'),
            ('tagType', 'all'),
        ]

        base = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?"
        response = requests.get(f"{base}{urlencode(query_string)}").json()

        results = [
            [
                currency["name"],
                round(currency["quotes"][0]["price"], 4),
                round(currency["quotes"][0]["percentChange1h"], 4),
                round(currency["quotes"][0]["percentChange24h"], 4),
                round(currency["quotes"][0]["percentChange7d"], 4),
                currency["quotes"][0]["marketCap"],
                currency["quotes"][0]["volume24h"]
                
                
                
                
            ]
            for currency in response["data"]["cryptoCurrencyList"]
        ]

        df = pd.DataFrame(results, columns=["name", "Price", "1h", "24h", "7d", "marketcap", "volume24" ])
        df_new=df.iloc[:,:].values
        lst= df_new.tolist()
        tuples = [tuple(x) for x in lst]
        records_to_insert =tuples
        msg=bulkInsert(records_to_insert)
        return HttpResponse(msg)
    else:
        return HttpResponse("method error")


class CoinView(APIView):
    def get(self,request, format=None):
        coin=CoinMarket.objects.all()
        serializer = CoinSerializer(coin, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


