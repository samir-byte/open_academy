
from odoo import models, fields, api

class Course(models.Model):
    _name = "openacademy.course"
    _description = "OpenAcademy Courses"

    name = fields.Char(string='Title', required=True, help='name of the course')
    description = fields.Text()
    responsible_id = fields.Many2one(
        'res.users',
        ondelete='set null',
        string='Responsible',
        index=True
        )
    session_ids = fields.One2many('openacademy.session', 'course_id',string='Sessions')


class Session(models.Model):
    _name = "openacademy.session"
    _description= "OpenAcademy Session"

    name  = fields.Char(required=True)
    start_date  = fields.Date()
    duration  = fields.Float(digits=(6,2), help='duration in days')
    seats  = fields.Integer(string='Number of seats')
    instructor_id = fields.Many2one(
        'res.partner',
        string='Instructor',
        )
    course_id = fields.Many2one(
        'openacademy.course',
        string='Course',
        ondelete='cascade',
        required=True
        )
    attendee_ids = fields.Many2many('res.partner', string='Attendees')
    taken_seats  = fields.Float(string='Taken Seats', compute='_taken_seats')

    @api.depends('seats','attendee_ids')
    def _taken_seats(self):
        for record in self:
            if not record.seats:
                record.taken_seats=0.0
            else:
                record.taken_seats=100.0 * len(record.attendee_ids) / record.seats 
    
    

