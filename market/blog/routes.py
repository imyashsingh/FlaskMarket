from flask import render_template,request,flash,redirect,url_for

from . import blog_bp
from market import db
from flask_login import  current_user, login_required

from market.models import Blog
from .forms import  BlogForm

@blog_bp.route('/market')
@blog_bp.route('/market_page')
def market_page():
    query = request.args.get('q')
    if query:
        blogs = Blog.query.filter(
            Blog.title.ilike(f"%{query}%") | Blog.content.ilike(f"%{query}%")).order_by(Blog.created_at.desc()).all()
    else:
        blogs = Blog.query.order_by(Blog.created_at.desc()).all()
        
    return render_template('blog/market.html', blogs=blogs)


# Blog detail route
@blog_bp.route('/blog/<int:blog_id>')
def blog_detail(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    if not blog:
        flash('Blog not found.', category='danger')
        return redirect(url_for('blog.market_page'))
    # Render the blog detail page with the blog data
    return render_template('blog/blog_detail.html', blog=blog)



# Create blog route
@blog_bp.route('/create_blog', methods=['GET', 'POST'])
@login_required
def create_blog():
    form=BlogForm()
    if form.validate_on_submit():
        new_blog = Blog(
            title=form.title.data,
            content=form.content.data,
            owner=current_user.id  # Associate the blog with the current user
        )
        db.session.add(new_blog)
        db.session.commit()
        flash(f'Blog "{new_blog.title}" created successfully!', category='success')
        return redirect(url_for('blog.market_page'))
    if form.errors:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating the blog: {err_msg}', category='danger')
    return render_template('blog/blog_form.html', form=form)

# Edit blog route
@blog_bp.route('/edit_blog/<int:blog_id>', methods=['GET', 'POST'])
@login_required
def edit_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)

    # Check ownership
    if blog.owner != current_user.id:
        flash('You do not have permission to edit this blog.', category='danger')
        return redirect(url_for('blog.market_page'))

    # Pre-fill form with blog data
    form = BlogForm(obj=blog)
    if form.validate_on_submit(): 
        form.populate_obj(blog)
        db.session.commit()
        flash(f'Blog "{blog.title}" updated successfully!', category='info')
        return redirect(url_for('blog.market_page'))

    return render_template('blog/blog_form.html', form=form, blog=blog)

# Delete blog route
@blog_bp.route('/delete_blog/<int:blog_id>', methods=['POST'])
@login_required
def delete_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)

    # Check ownership
    if blog.owner != current_user.id:
        flash('You do not have permission to delete this blog.', category='danger')
        return redirect(url_for('blog.market_page'))
    db.session.delete(blog)
    db.session.commit()
    flash(f'Blog "{blog.title}" deleted successfully!', category='danger')
    return redirect(url_for('blog.market_page'))
