from django.shortcuts import render
from django.http import HttpResponse
from .models import Profile, Skill, Education, Project, Training, Language
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, HRFlowable, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
from django.conf import settings
import os

# Register custom fonts
font_path = os.path.join(settings.BASE_DIR, 'fonts')
pdfmetrics.registerFont(TTFont('Poppins', os.path.join(font_path, 'Poppins-Regular.ttf')))
pdfmetrics.registerFont(TTFont('Poppins-Bold', os.path.join(font_path, 'Poppins-Bold.ttf')))
pdfmetrics.registerFont(TTFont('Roboto', os.path.join(font_path, 'Roboto-Regular.ttf')))
pdfmetrics.registerFont(TTFont('Roboto-Bold', os.path.join(font_path, 'Roboto-Bold.ttf')))

def resume(request):
    profile = Profile.objects.first()
    skills = Skill.objects.all()
    educations = Education.objects.all()
    projects = Project.objects.all()
    trainings = Training.objects.all()
    languages = Language.objects.all()
    context = {
        'profile': profile,
        'skills': skills,
        'educations': educations,
        'projects': projects,
        'trainings': trainings,
        'languages': languages,
    }
    return render(request, 'resume_app/resume.html', context)

def download_pdf(request):
    profile = Profile.objects.first()
    skills = Skill.objects.all().order_by('category')
    educations = Education.objects.all()
    projects = Project.objects.all()
    trainings = Training.objects.all()
    languages = Language.objects.all()

    # Create PDF
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=0.75*inch, rightMargin=0.75*inch, topMargin=0.75*inch, bottomMargin=0.75*inch)
    styles = getSampleStyleSheet()

    # Custom styles with purple and fonts
    styles.add(ParagraphStyle(
        name='TitlePurple', fontName='Poppins-Bold', fontSize=20, textColor=HexColor('#8b5cf6'), alignment=0, spaceAfter=8
    ))
    styles.add(ParagraphStyle(
        name='Heading2Purple', fontName='Roboto-Bold', fontSize=12, textColor=HexColor('#8b5cf6'), spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        name='Heading1Purple', fontName='Roboto-Bold', fontSize=14, textColor=HexColor('#6b21a8'), spaceAfter=10
    ))
    styles.add(ParagraphStyle(
        name='NormalGray', fontName='Poppins', fontSize=10, textColor=HexColor('#666666'), leading=14, spaceBefore=4
    ))
    styles.add(ParagraphStyle(
        name='BulletGray', fontName='Poppins', fontSize=10, textColor=HexColor('#666666'), leftIndent=10, bulletIndent=0, leading=12
    ))

    story = []

    # Header with photo on left and details on right
    if profile.photo and os.path.exists(profile.photo.path):
        photo = Image(profile.photo.path, width=1.5*inch, height=1.5*inch)
        photo_data = [[photo]]
        photo_table = Table(photo_data, colWidths=[1.5*inch], rowHeights=[1.5*inch])
        photo_table.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 2, HexColor('#8b5cf6')),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
    else:
        photo_table = Table([[""]], colWidths=[1.5*inch])  # Placeholder if no photo

    header_text = [
        Paragraph(f"{profile.name}", styles['TitlePurple']),
        Paragraph(f"{profile.title}", styles['Heading2Purple']),
        Paragraph(f"Email: {profile.email} | Phone: {profile.phone}", styles['NormalGray']),
        Paragraph(f"LinkedIn: {profile.linkedin}", styles['NormalGray']),
        Paragraph(f"Location: {profile.location}", styles['NormalGray']),
    ]
    header_data = [[photo_table, header_text]]
    header_table = Table(header_data, colWidths=[1.5*inch, 4.5*inch])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (1, 0), (1, -1), 12),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#8b5cf6'), spaceAfter=20))

    # Summary
    story.append(Paragraph("Summary", styles['Heading1Purple']))
    story.append(Paragraph(profile.summary, styles['NormalGray']))
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#8b5cf6'), spaceAfter=20))

    # Skills - Grouped with bullets
    story.append(Paragraph("Skills", styles['Heading1Purple']))
    skill_groups = {}
    for skill in skills:
        if skill.category not in skill_groups:
            skill_groups[skill.category] = []
        skill_groups[skill.category].append(skill.name)
    
    for category, names in skill_groups.items():
        story.append(Paragraph(category, styles['Heading2Purple']))
        for name in names:
            story.append(Paragraph(f"• {name}", styles['BulletGray']))
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#8b5cf6'), spaceAfter=20))

    # Projects
    story.append(Paragraph("Projects", styles['Heading1Purple']))
    for project in projects:
        story.append(Paragraph(project.title, styles['Heading2Purple']))
        story.append(Paragraph(project.description, styles['NormalGray']))
        story.append(Paragraph(f"Technologies: {project.technologies}", styles['NormalGray']))
        story.append(Spacer(1, 10))
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#8b5cf6'), spaceAfter=20))

    # Education
    story.append(Paragraph("Education", styles['Heading1Purple']))
    for edu in educations:
        story.append(Paragraph(f"{edu.degree} - {edu.institution}", styles['Heading2Purple']))
        story.append(Paragraph(f"{edu.duration} | CGPA: {edu.cgpa}%", styles['NormalGray']))
        story.append(Spacer(1, 10))
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#8b5cf6'), spaceAfter=20))

    # Training / Courses - With bullets
    story.append(Paragraph("Training / Courses", styles['Heading1Purple']))
    for training in trainings:
        story.append(Paragraph(f"• {training.name}", styles['BulletGray']))
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=HexColor('#8b5cf6'), spaceAfter=20))

    # Languages - With bullets
    story.append(Paragraph("Languages", styles['Heading1Purple']))
    for language in languages:
        story.append(Paragraph(f"• {language.name}", styles['BulletGray']))

    # Build with custom border
    def add_border(canvas, doc):
        canvas.setStrokeColor(HexColor('#8b5cf6'))
        canvas.setLineWidth(1)
        canvas.rect(0.5*inch, 0.5*inch, letter[0]-inch, letter[1]-inch, fill=0)

    doc.build(story, onFirstPage=add_border, onLaterPages=add_border)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Anandhu_TS_Resume.pdf"'
    return response