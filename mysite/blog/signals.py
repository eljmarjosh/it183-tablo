from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.core.exceptions import PermissionDenied
from .models import Post, Comment

@receiver(pre_save, sender=Comment)
def check_comment_author_update(sender, instance, **kwargs):
    """
    Ensure the user updating a comment is the author of the comment.
    """
    if instance.pk:  # Check if the comment already exists (update operation)
        original_comment = Comment.objects.get(pk=instance.pk)
        if original_comment.author != instance.author:
            raise PermissionDenied("You are not authorized to update this comment.")


@receiver(pre_delete, sender=Comment)
def check_comment_author_delete(sender, instance, **kwargs):
    """
    Ensure the user deleting a comment is the author of the comment.
    """
    if instance.author != instance.author:
        raise PermissionDenied("You are not authorized to delete this comment.")


@receiver(pre_save, sender=Post)
def check_post_author_update(sender, instance, **kwargs):
    """
    Ensure the user updating a post is the author of the post.
    """
    if instance.pk:  # Check if the post already exists (update operation)
        original_post = Post.objects.get(pk=instance.pk)
        if original_post.author != instance.author:
            raise PermissionDenied("You are not authorized to update this post.")


@receiver(pre_delete, sender=Post)
def check_post_author_delete(sender, instance, **kwargs):
    """
    Ensure the user deleting a post is the author of the post.
    """
    if instance.author != instance.author:
        raise PermissionDenied("You are not authorized to delete this post.")
