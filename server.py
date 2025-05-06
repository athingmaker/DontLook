from flask import Flask, request, render_template_string

app = Flask(__name__)
received_requests = []

@app.route('/', methods=['GET', 'POST'])
def handle_requests():
    if request.method == 'POST':
        # Get data from different content types
        if request.is_json:
            data = request.json
        elif request.form:
            data = dict(request.form)
        else:
            data = request.data.decode('utf-8')
        
        received_requests.append({
            'method': request.method,
            'path': request.path,
            'headers': dict(request.headers),
            'data': data
        })
    
    return render_template_string(HTML_TEMPLATE, requests=received_requests)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Request Monitor</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .request { border: 1px solid #ddd; padding: 15px; margin-bottom: 10px; border-radius: 5px; }
        .method { font-weight: bold; color: #007bff; }
        .path { color: #28a745; }
        pre { background: #f8f9fa; padding: 10px; border-radius: 3px; }
    </style>
</head>
<body>
    <h1>Received Requests</h1>
    {% if not requests %}
        <p>No requests received yet.</p>
    {% endif %}
    {% for req in requests %}
        <div class="request">
            <div><span class="method">{{ req.method }}</span> <span class="path">{{ req.path }}</span></div>
            <h3>Headers:</h3>
            <pre>{{ req.headers | tojson(indent=2) }}</pre>
            <h3>Data:</h3>
            <pre>{{ req.data | tojson(indent=2) if req.data is mapping or req.data is sequence else req.data }}</pre>
        </div>
    {% endfor %}
</body>
</html>
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
