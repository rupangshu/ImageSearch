from imageWrap import SearchImageWrap
from flask import Flask,redirect,url_for,request,render_template
from MongoDBUtil import MongoPersist
import sys
app = Flask(__name__)

@app.route('/searchKeyword',methods=['POST'])
def imageSearch():
    if request.method == 'POST':
        keyword = request.form['keyword']
        searchImageBean = SearchImageWrap()
        result = 'Successfully fetch all results related to the keyword '+keyword
        try:
             searchImageBean.searchImg(keyword)
        except Exception as e:
           result='Not able to process you request.Please try after sometime.'
        return render_template("status.html", result=result)


@app.route('/searchResults')
def reviewsearch():
    if request.method == 'GET':
        query = request.args.get('keyword')
        result = "query results found"
        try:
            searchImageBean = SearchImageWrap()
            result = searchImageBean.getdetails(query)
        except Exception as e:
            print(e)
            result = 'Not able to process you request.Please try after sometime.'
        return render_template("searchResults.html", result=result)

if __name__ == '__main__':
    app.run(debug= True)
