import os
import bpy

bl_info = {
    "name": "Export Audio Tracks",
    "author": "John Galt",
    "version": (1, 0),
    "blender": (3, 5, 1),
    "location": "Sequencer > Export",
    "description": "Export each audio track as a separate audio file for mixing in your DAW",
    "category": "Sequencer",
}

# Operator for exporting audio track
class ExportAudioTrackOperator(bpy.types.Operator):
    bl_idname = "sequencer.export_audio_track"
    bl_label = "Export Audio Track"
    
    def execute(self, context):
        scene = context.scene
        
        # Store the original mute states of the strips
        original_mute_states = {}
        for strip in scene.sequence_editor.sequences_all:
            if strip.type == 'SOUND':
                original_mute_states[strip.channel] = strip.mute
        
        # Loop through each channel containing audio strips
        for channel_number in original_mute_states:
            # Mute all other channels
            for strip in scene.sequence_editor.sequences_all:
                if strip.type == 'SOUND':
                    strip.mute = strip.channel != channel_number
            
            # Set output path and file name
            output_path = scene.export_audio_output_path
            audio_container = scene.export_audio_container
            channel_name = f"Channel_{channel_number}"
            file_name = f"{channel_name}.{audio_container.lower()}"
            output_file_path = os.path.join(output_path, file_name)
            
            # Set sample rate
            sample_rate = scene.export_audio_sample_rate
            
            # Set render settings
            scene.render.image_settings.file_format = 'FFMPEG'
            scene.render.ffmpeg.audio_codec = audio_container
            scene.render.ffmpeg.audio_bitrate = 192
            
            # Delete existing output file if it exists
            if os.path.exists(output_file_path):
                os.remove(output_file_path)
            
            # Render audio track
            bpy.ops.sound.mixdown(
                filepath=output_file_path,
                codec=audio_container,
                container=audio_container,
            )
        
        # Restore the original mute states of the strips
        for strip in scene.sequence_editor.sequences_all:
            if strip.type == 'SOUND':
                strip.mute = original_mute_states.get(strip.channel, False)
        
        self.report({'INFO'}, "Audio Tracks Exported Successfully!")
        return {'FINISHED'}

# Panel for the Export tab
class ExportPanel(bpy.types.Panel):
    bl_idname = "SEQUENCER_PT_export_panel"
    bl_label = "Export"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Export'
    
    def draw(self, context):
        layout = self.layout
        
        # File output path
        layout.label(text="Output Path:")
        row = layout.row(align=True)
        row.prop(context.scene, "export_audio_output_path", text="", icon='FILE_FOLDER')
        
        # Sample Rate
        layout.label(text="Sample Rate:")
        layout.prop(context.scene, "export_audio_sample_rate", text="")
        
        # Audio container dropdown
        layout.label(text="Audio Container:")
        layout.prop(context.scene, "export_audio_container", text="")
        
        # Export button
        layout.operator("sequencer.export_audio_track", text="Export Audio Track")

# Register the classes
classes = [
    ExportAudioTrackOperator,
    ExportPanel,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.export_audio_output_path = bpy.props.StringProperty(
        name="Output Path",
        default="",
        subtype='DIR_PATH',
    )
    bpy.types.Scene.export_audio_sample_rate = bpy.props.IntProperty(
        name="Sample Rate",
        default=44100,
        min=1,
    )
    bpy.types.Scene.export_audio_container = bpy.props.EnumProperty(
        name="Audio Container",
        items=[
            ('MP3', 'MP3', ''),
            ('FLAC', 'FLAC', ''),
        ],
        default='FLAC',
    )

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
    del bpy.types.Scene.export_audio_output_path
    del bpy.types.Scene.export_audio_sample_rate
    del bpy.types.Scene.export_audio_container

if __name__ == "__main__":
    register()

