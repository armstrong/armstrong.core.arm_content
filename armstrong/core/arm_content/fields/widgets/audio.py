from django.utils.html import escape, conditional_escape

from django.forms.widgets import ClearableFileInput

class AudioFileWidget(ClearableFileInput):

    class Media:
        js = ('jplayer.js' ,)
    
    template_player = """
        <div id="%(playerdivid)" class="jp-jplayer"></div>

        <script type="text/javascript">
        //<![CDATA[
        $(document).ready(function(){
            $("#jquery_jplayer_1").jPlayer({
                ready: function () {
                    $(this).jPlayer("setMedia", {
                        %(format): "%(url)"
                    },
                    swfPath: "../js",
                    supplied: "%(format)"
                }).jPlayer("load");   
            });
        //]]>
        """

    def jplayer_format(self):
        if( value.format):
            pass

    def player_id(self, name):
       return name + '_player_id'

    def render(self,name, value, attrs):
        parrent_output=super(AudioFileWidget, selfi).render(name, value, attrs)

        data={ 'playerdivid' : conditional_escape(self.player_id(name)),
               'format' : conditional_escape(value.audioformat),
               'url': conditional_escape(value.url),
            }
        return mark_safe(parrent_output + (template_player % data))
