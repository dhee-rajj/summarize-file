from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import UploadedFile
import pandas as pd

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = UploadedFile(file=request.FILES['file'])
            uploaded_file.save()
            return redirect('summary_report', file_id=uploaded_file.id)
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def summary_report(request, file_id):
    uploaded_file = UploadedFile.objects.get(id=file_id)
    try:
        # Check the file extension and read the file accordingly
        if uploaded_file.file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file.file.path, encoding='utf-8', delimiter=',', on_bad_lines='skip')
        elif uploaded_file.file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(uploaded_file.file.path)
        else:
            return render(request, 'summary.html', {'error': 'Uploaded file is not a supported format. Please upload a CSV or Excel file.'})
    except UnicodeDecodeError:
        df = pd.read_csv(uploaded_file.file.path, encoding='ISO-8859-1', delimiter=',', on_bad_lines='skip')
    except pd.errors.ParserError as e:
        return render(request, 'summary.html', {'error': f'Error parsing file: {e}'})
    except Exception as e:
        return render(request, 'summary.html', {'error': f'An unexpected error occurred: {e}'})
    
    # Debugging: Check if DataFrame is empty
    if df.empty:
        return render(request, 'summary.html', {'error': 'The uploaded file is empty or could not be read correctly.'})
    
    # Debugging: Check DataFrame columns
    columns = df.columns.tolist()
    if len(columns) < 3:
        return render(request, 'summary.html', {'error': 'The uploaded file does not have enough columns.'})
    
    # Get the last 3 columns of the DataFrame
    summary = df.iloc[:, -3:].to_html()
    return render(request, 'summary.html', {'summary': summary, 'columns': columns, 'debug': df.head().to_html()})