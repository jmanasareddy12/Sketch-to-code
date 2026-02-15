def generate_html(detections):
    """
    Takes a list of detections and returns a full HTML string.
    """
    # Start the HTML document
    html_string = """
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Generated Page</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container py-5">
    """
    
    # Loop through the sorted detections
    for item in detections:
        if item['class'] == 'paragraph':
            html_string += '<div class="row mb-3"><div class="col-md-8 mx-auto"><p class="lead">Sample paragraph text.</p></div></div>\n'
            
        elif item['class'] == 'image':
            html_string += '<div class="row mb-3"><div class="col-md-8 mx-auto"><img src="https://placehold.co/600x400" class="img-fluid rounded"></div></div>\n'
            
        elif item['class'] == 'text-input':
            html_string += '<div class="row mb-3"><div class="col-md-8 mx-auto"><input type="text" class="form-control" placeholder="Enter data here..."></div></div>\n'
        
        # ---
        # ⚠️ THIS IS THE BUG FIX ---
        # You need to add the logic for your button!
        # ---
        elif item['class'] == 'button':
            html_string += '<div class="row mb-3"><div class="col-md-8 mx-auto text-center"><button type="submit" class="btn btn-primary">Submit</button></div></div>\n'
            
    # Close the HTML document
    html_string += """
        </div>
    </body>
    </html>
    """
    
    return html_string