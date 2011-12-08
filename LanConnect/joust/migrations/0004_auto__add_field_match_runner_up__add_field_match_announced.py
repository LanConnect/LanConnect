# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Match.runner_up'
        db.add_column('joust_match', 'runner_up', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_matches_placed', null=True, to=orm['joust.Entrant']), keep_default=False)

        # Adding field 'Match.announced'
        db.add_column('joust_match', 'announced', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Match.runner_up'
        db.delete_column('joust_match', 'runner_up_id')

        # Deleting field 'Match.announced'
        db.delete_column('joust_match', 'announced')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'joust.entrant': {
            'Meta': {'ordering': "['team_name', 'primary_user__username']", 'object_name': 'Entrant'},
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['joust.Event']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['joust.Location']", 'null': 'True', 'blank': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'members'", 'blank': 'True', 'to': "orm['auth.User']"}),
            'photo': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'primary_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'primary_user'", 'to': "orm['auth.User']"}),
            'skill': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'team_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'})
        },
        'joust.event': {
            'Meta': {'ordering': "['start', 'name']", 'object_name': 'Event'},
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_progress': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'organiser': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        },
        'joust.game': {
            'Meta': {'ordering': "['name']", 'object_name': 'Game'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'platform': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'})
        },
        'joust.location': {
            'Meta': {'ordering': "['name']", 'object_name': 'Location'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'joust.match': {
            'Meta': {'object_name': 'Match'},
            'announced': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'entrants': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'_matches_entered'", 'symmetrical': 'False', 'to': "orm['joust.Entrant']"}),
            'finished': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'runner_up': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_matches_placed'", 'null': 'True', 'to': "orm['joust.Entrant']"}),
            'runner_up_next': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_runner_up'", 'null': 'True', 'to': "orm['joust.Match']"}),
            'started': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'station': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'_stations'", 'null': 'True', 'to': "orm['joust.Station']"}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'matches'", 'to': "orm['joust.Tournament']"}),
            'winner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_matches_won'", 'null': 'True', 'to': "orm['joust.Entrant']"}),
            'winner_next': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from_winner'", 'null': 'True', 'to': "orm['joust.Match']"})
        },
        'joust.station': {
            'Meta': {'ordering': "['name']", 'object_name': 'Station'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['joust.Event']"}),
            'games': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['joust.Game']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'joust.tournament': {
            'Meta': {'ordering': "['start', 'name']", 'object_name': 'Tournament'},
            'bracket_type': ('django.db.models.fields.CharField', [], {'default': "'se'", 'max_length': '2'}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'entrants': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['joust.Entrant']", 'null': 'True', 'blank': 'True'}),
            'entrants_per_match': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tournaments_run'", 'to': "orm['joust.Event']"}),
            'finished_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tournament_games'", 'to': "orm['joust.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_entrants': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'players_per_entrant': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'root_match': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_root_tournament'", 'null': 'True', 'to': "orm['joust.Match']"}),
            'seed_type': ('django.db.models.fields.CharField', [], {'default': "'r'", 'max_length': '1'}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'started_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['joust']
