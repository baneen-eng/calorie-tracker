from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__ )

foods = pd.read_csv('data/foods.csv')

@app.route('/')
def index():
    query = request.args.get('q', '')
    cat = request.args.get('cat', '')
    
    result = foods
    
    if query:
        result = result[result['description'].str.contains(query, case=False, na=False)]
    
    if cat:
        result = result[result['category'] == cat]
    
    categories = sorted(foods['category'].unique())
    
    return render_template('foods.html', foods=result.to_dict('records'), categories=categories, selected_cat=cat, query=query)

if __name__ == '__main__':
    app.run(debug=True)

    