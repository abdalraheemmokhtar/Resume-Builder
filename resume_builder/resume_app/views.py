from django.shortcuts import render, redirect
from docx import Document
from django.http import HttpResponse
from .forms import CVForm
import torch
from transformers import pipeline
import accelerate


# Create your views here.
def home(request):
    return render(request, 'home.html')

def other_view(request):
    combined_text = None

    if request.method == 'POST':
        form = CVForm(request.POST)
        if form.is_valid():
            # Concatenate text from both text areas
            combined_text = f"{form.cleaned_data['content']}\n\n{form.cleaned_data['desired_role']}"

            # If a download parameter is present, save the text to a file and serve it for download
            if request.GET.get('download'):
                filename = "combined_cv.txt"
                with open(filename, 'w') as file:
                    file.write(combined_text)

                with open(filename, 'r') as file:
                    response = HttpResponse(file.read(), content_type='text/plain')
                    response['Content-Disposition'] = f'attachment; filename={filename}'
                    return response
    else:
        form = CVForm()

    return render(request, 'body.html', {'form': form, 'combined_text': combined_text or ''})

def download_cv(request):
    combined_text = None

    if request.method == 'GET':
        # Fetch the combined text from wherever it's stored
        # You might want to consider storing it in a database or some other persistent storage
        combined_text = "Combined text fetched from storage"  # Replace this with your actual logic

        # Serve the text as a downloadable file
        filename = "combined_cv.txt"
        response = HttpResponse(combined_text, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response

    return HttpResponse("Invalid request method")

def generate_text(request):
    if request.method == 'POST':
        input_text = request.POST.get('input_text', '')
        pipe = pipeline("text-generation", model="HuggingFaceH4/zephyr-7b-alpha", torch_dtype=torch.bfloat16, device_map="auto")
        messages = [
    {
        "role": "system",
        "content": "You are a friendly chatbot who always responds in the style of a pirate",
    },
         {"role": "user", "content": input_text},
                    ]
        prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False,low_cpu_mem_usage=True, add_generation_prompt=True)
        outputs = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
        generated_text = outputs[0]["generated_text"]

        return render(request, 'hug.html', {'input_text': input_text, 'generated_text': generated_text})

    return render(request, 'hug.html')