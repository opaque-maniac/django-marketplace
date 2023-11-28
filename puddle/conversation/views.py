from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .forms import ConverationMessageForm
from item.models import Item
from .models import Conversation

# Create your views here.
@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)
    if item.created_by == request.user:
        return redirect('item:detail', pk=item_pk)
    conversations = Conversation.objects.filter(item=item).filter(members__in=[request.user])
    if conversations:
        pass

    if request.method == 'POST':
        form = ConverationMessageForm(data=request.POST)
        if form.is_valid():

            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.created_by)
            conversation.save()

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('item:detail', pk=item_pk)
    else:
        form = ConverationMessageForm()

    context = {
        'form': form,
    }
    return render(request, 'conversation/new.html', context)

@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user])
    context = {
        'conversations': conversations,
    }
    return render(request, 'conversation/inbox.html', context)

@login_required
def detail(request, pk):
    conversation = Conversation.objects.filter(members__in=[request.user]).get(pk=pk)
    context = {
        'conversation': conversation,
    }
    return render(request, 'conversation/detail.html', context)