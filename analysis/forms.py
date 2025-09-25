from django import forms

class PGNUploadForm(forms.Form):
    pgn_file = forms.FileField(label="Upload PGN File")
