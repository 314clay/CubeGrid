from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

def getData():
    column_names = ['Goal', 'Set', 'Subset', 'Alg', 'Learned?', 'Link']
    df = pd.read_csv('Algsheet.csv', header=None, names=column_names)

    # Drop first row
    df = df.drop(index=0)

    # Drop rows with missing Alg values
    df.drop(df[(df['Alg'].isnull()) | (df['Alg'] == '') | (df['Alg'].apply(lambda x: isinstance(x, float)))].index, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df['Alg'] = df['Alg'].apply(lambda x: x.split('\n')[0])

    # Create a function to concatenate the values of 'Goal', 'Set', and 'Subset' columns with a space
    def make_title(row):
        title_parts = []
        if isinstance(row['Goal'], str):
            title_parts.append(row['Goal'].title())
        if isinstance(row['Set'], str):
            title_parts.append(row['Set'].title())
        if isinstance(row['Subset'], str):
            title_parts.append(row['Subset'].title())
        return f"{' '.join(title_parts)}: {row['Alg']}"

    df['Title'] = df.apply(make_title, axis=1)

    alg_mod = df['Alg'].str.replace('Anti-Diag: ', '').str.replace('AUF Trick: ', '')
    url_prefix = 'http://cube.rider.biz/visualcube.php?fmt=svg&bg=silver&view=plan&stage=zbll&case='
    df['image_url'] = url_prefix + alg_mod

    df = df.rename(columns={
        'Learned?': 'learned',
        'Link': 'link',
        'Title': 'title',
        'image_url': 'image_url'
    })
    df["learned"] = df["learned"].fillna(False).astype(bool)

    pd.set_option('display.max_columns', None)
    df.to_csv("output.csv")
    return df

@app.route('/', methods=['GET', 'POST'])
def index():
    # if request.method == 'POST':
    #     search_term = request.form['search']
    #     filtered_df = df[df['title'].str.contains(search_term, case=False)]
    #     filtered_elements = filtered_df.to_dict('records')
    #     return render_template('index.html', elements=filtered_elements)
    elements = getData().to_dict('records')
    return render_template('index.html', elements=elements)


if __name__ == '__main__':
    app.run(debug=True)