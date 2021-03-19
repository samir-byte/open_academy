
from datetime import timedelta
from odoo import exceptions, models, fields, api

class Course(models.Model):
    #name and description of course model
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

    #sql constraints 
    _sql_constraints = [
        (
            'name_description_check',
            'CHECK(name != description)',
            'The title of course should not be the description'
        ),
        (
            'name_unique',
            'UNIQUE(name)',
            'The course title must be unique'
        )
    ]


class Session(models.Model):
    #name and description of model
    _name = "openacademy.session"
    _description= "OpenAcademy Session"

    #fields defined for session model
    name  = fields.Char(required=True)
    #start_date  = fields.Date()
    start_date  = fields.Date(default=fields.Date.today()) #adding default date of current date 
    duration  = fields.Float(digits=(6,2), help='duration in days')
    seats  = fields.Integer(string='Number of seats')
    active  = fields.Boolean(default= True)
    instructor_id = fields.Many2one(#field many2one implemented 
        'res.partner',
        string='Instructor',
        )
    course_id = fields.Many2one(
        'openacademy.course',
        string='Course',
        ondelete='cascade',
        required=True
        )
    attendee_ids = fields.Many2many('res.partner', string='Attendees') #field many2many implemented
    
    #new field this depends on seats and attendee_ids field
    taken_seats  = fields.Float(string='Taken Seats', compute='_taken_seats')
    date_end  = fields.Date(string="End Date", store=True, compute='_get_end_date', inverse='_set_end_date')
    
    #computed fields and @api.depends
    @api.depends('seats','attendee_ids')
    def _taken_seats(self):
        #for loop to find taken seats
        for record in self:
            if not record.seats:
                record.taken_seats=0.0
            else:
                record.taken_seats=100.0 * len(record.attendee_ids) / record.seats 

    #@api.onchange implemented on the fields seats and attendee_ids
    @api.onchange('seats','attendee_ids')
    def _verify_valid_seats(self):
        
        if (self.seats < 0 ) :
            return {
                'warning': {
                    'title': 'Too many Attendee',
                    'message': 'The number of seats availbale cant be in negative',
                }
            }
        if (self.seats < len(self.attendee_ids)):
            return {
                'warning': {
                    'title': 'Too many Attendee',
                    'message': 'increase seats or remove access attendees',
                }
            }


    #model constrains @api.constrains implemented
    @api.constrains('instructor_id','attendee_ids')
    def _check_instructor_not_in_attendee(self):
        for record in self:
            if (record.instructor_id and record.instructor_id in record.attendee_ids):
                raise exceptions.ValidationError("A session's instructor cant be an attendee")

    
    #methods to get end date
    @api.depends('start_date','duration')
    def _get_end_date(self):
        for record in self:
            if not (record.start_date and record.duration):
                record.date_end = record.start_date
                continue

            duration = timedelta(days=record.duration, seconds=-1)
            record.date_end = record.start_date + duration

    def _set_end_date(self):
        for record in self:
            if not(record.start_date and record.end_date):
                continue

            record.duration = (record.date_end - record.start_date).days +1
    
    

