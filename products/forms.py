from django import forms
from .models import Review, Comment

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["text", "rating"]
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "class": "form-control mb-2",
                    "rows": 3,
                    "placeholder": "Fikringizni yozing..."
                }
            ),
            "rating": forms.RadioSelect(
                choices=[(i, str(i)) for i in range(1, 6)],
                attrs={"class": "d-none"}  # yashiramiz, faqat yulduzchalarni ishlatamiz
            ),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(
                attrs={
                    "class": "form-control mb-2",
                    "rows": 3,
                    "placeholder": "Kommentariya yozing..."
                }
            )
        }
