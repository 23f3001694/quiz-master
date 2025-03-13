import matplotlib
matplotlib.use('Agg')  # Set the backend before importing pyplot
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime, timedelta

def get_base64_chart(fig):
    """Convert matplotlib figure to base64 string for HTML embedding"""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=300)
    buf.seek(0)
    string = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return f'data:image/png;base64,{string}'

def generate_user_performance_chart(scores):
    """Generate line chart showing user's performance over time"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if not scores:
        ax.text(0.5, 0.5, 'No quiz data available', 
                horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes)
        return get_base64_chart(fig)
    
    # Sort scores by date to ensure correct chronological order
    scores = sorted(scores, key=lambda x: x.quiz.date_of_quiz)
    
    dates = [score.quiz.date_of_quiz for score in scores]
    percentages = []
    
    for score in scores:
        try:
            percentage = (score.total_score / score.max_score * 100) if score.max_score > 0 else 0
            percentages.append(percentage)
        except (ZeroDivisionError, TypeError):
            percentages.append(0)
    
    # Create single line plot with connected points
    ax.plot(dates, percentages, 'b-o', linewidth=2, markersize=6)
    
    ax.set_title('Performance Over Time')
    ax.set_xlabel('Quiz Date')
    ax.set_ylabel('Score (%)')
    ax.grid(True)
    
    # Set y-axis limits from 0 to 100
    ax.set_ylim(0, 100)
    
    plt.xticks(rotation=45)
    plt.tight_layout()  # Adjust layout to prevent label cutoff
    
    return get_base64_chart(fig)

def generate_subject_performance_chart(subject_scores):
    """Generate bar chart showing performance by subject"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if not subject_scores:
        ax.text(0.5, 0.5, 'No subject data available', 
                horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes)
        return get_base64_chart(fig)
    
    subjects = list(subject_scores.keys())
    avg_scores = []
    
    for scores in subject_scores.values():
        try:
            if scores:
                percentages = [score['percentage'] for score in scores]
                avg_score = sum(percentages) / len(percentages) if percentages else 0
            else:
                avg_score = 0
            avg_scores.append(avg_score)
        except (ZeroDivisionError, TypeError):
            avg_scores.append(0)
    
    ax.bar(subjects, avg_scores)
    ax.set_title('Average Performance by Subject')
    ax.set_xlabel('Subject')
    ax.set_ylabel('Average Score (%)')
    
    plt.xticks(rotation=45)
    
    return get_base64_chart(fig)

def generate_admin_quiz_stats(quizzes):
    """Generate charts for admin quiz statistics"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    dates = [quiz.date_of_quiz for quiz in quizzes]
    participants = [len(quiz.scores) for quiz in quizzes]
    
    ax1.plot(dates, participants, marker='o')
    ax1.set_title('Quiz Participation Over Time')
    ax1.set_xlabel('Quiz Date')
    ax1.set_ylabel('Number of Participants')
    ax1.grid(True)
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
    
    avg_scores = []
    for quiz in quizzes:
        if quiz.scores:
            scores = [(score.total_score / score.max_score * 100) for score in quiz.scores]
            avg_scores.append(sum(scores) / len(scores))
        else:
            avg_scores.append(0)
    
    ax2.hist(avg_scores, bins=10, edgecolor='black')
    ax2.set_title('Distribution of Average Quiz Scores')
    ax2.set_xlabel('Average Score (%)')
    ax2.set_ylabel('Number of Quizzes')
    ax2.grid(True)
    
    plt.tight_layout()
    return get_base64_chart(fig)

def generate_admin_user_stats(users):
    """Generate charts for admin user statistics"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    quiz_counts = [len(user.scores) for user in users]
    
    ax1.hist(quiz_counts, bins=max(10, max(quiz_counts)//5), edgecolor='black')
    ax1.set_title('Distribution of User Activity')
    ax1.set_xlabel('Number of Quizzes Taken')
    ax1.set_ylabel('Number of Users')
    ax1.grid(True)
    
    avg_performances = []
    for user in users:
        if user.scores:
            scores = [(score.total_score / score.max_score * 100) for score in user.scores]
            avg_performances.append(sum(scores) / len(scores))
    
    if avg_performances:
        ax2.hist(avg_performances, bins=10, edgecolor='black')
        ax2.set_title('Distribution of User Performance')
        ax2.set_xlabel('Average Score (%)')
        ax2.set_ylabel('Number of Users')
        ax2.grid(True)
    
    plt.tight_layout()
    return get_base64_chart(fig) 