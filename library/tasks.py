import datetime

from celery import shared_task
from .models import Loan
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned Successfully',
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass


@shared_task
def check_overdue_loans():
    try:
        due_loans = Loan.objects.filter(due_date__lt=datetime.date.today(), is_returned=False)
        for loan in due_loans:
            send_mail(
                subject=f"Overdue book: {loan.book.title}",
                message=f"Hello {loan.member.user.username},\n\nYou loan has due on {loan.due_date}.\n\nPlease return the book.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[loan.member.user.email],
                fail_silently=False
            )
    except:
        pass