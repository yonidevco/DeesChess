from django import forms

class PGNUploadForm(forms.Form):
    file = forms.FileField(
        label="",
        widget=forms.ClearableFileInput(attrs={
            "id": "fileInput",        
            "accept": ".pgn,.txt",    
            "style": "display:none;",
        })
    )
