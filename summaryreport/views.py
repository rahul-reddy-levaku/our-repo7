import pandas as pd
from django.shortcuts import render
from .forms import UploadFileForm


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            try:
                # Specify the engine explicitly
                df = pd.read_excel(file, engine='openpyxl')
            except Exception as e:
                # Handle the case where the file might not be Excel or needs a different engine
                return render(request, 'summaryreport/summary.html', {'error': str(e)})

            summary = df.groupby(['Cust State']).agg({'DPD': ['count', 'sum']}).reset_index()
            summary.columns = ['Cust State', 'Number of Customers', 'Total DPD']
            return render(request, 'summaryreport/summary.html', {'summary': summary.to_html(index=False)})
    else:
        form = UploadFileForm()
    return render(request, 'summaryreport/upload.html', {'form': form})

