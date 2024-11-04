# # import numpy as np
# # import librosa
# # import matplotlib.pyplot as plt
# #
# # # Function to detect notes from audio
# # def detect_notes(audio, sr):
# #     pitches, magnitudes = librosa.piptrack(y=audio, sr=sr)
# #     notes = []
# #     for t in range(pitches.shape[1]):
# #         index = magnitudes[:, t].argmax()
# #         pitch = pitches[index, t]
# #         if pitch > 0:  # Consider only valid pitches
# #             time = librosa.frames_to_time(t, sr=sr)
# #             notes.append((pitch, time))
# #     return notes
# #
# # # Convert pitch to numbered notation (based on C-major as 1=C)
# # def pitch_to_notation(pitch):
# #     note = librosa.hz_to_note(pitch)
# #     note_map = {'C': '1', 'D': '2', 'E': '3', 'F': '4', 'G': '5', 'A': '6', 'B': '7'}
# #     octave = int(note[-1])  # Extract octave number
# #     notation = note_map.get(note[:-1], '?')  # Map note name to number
# #     return f"{notation}"  # Customize if octave needed (e.g., f"{notation}({octave})")
# #
# # # Plotting the numbered musical notation
# # def plot_simplified_score(notes, output_image):
# #     fig, ax = plt.subplots(figsize=(10, 4))
# #     plt.axis('off')
# #
# #     # Organize notes into lines
# #     line_length = 8  # Number of notes per line
# #     lines = [notes[i:i + line_length] for i in range(0, len(notes), line_length)]
# #
# #     # Plot each line of the musical score
# #     for i, line in enumerate(lines):
# #         for j, (pitch, time) in enumerate(line):
# #             notation = pitch_to_notation(pitch)
# #             ax.text(j * 2, -i * 1.5, notation, fontsize=20, ha='center', va='center')
# #
# #     plt.xlim(-1, line_length * 2)
# #     plt.ylim(-len(lines) * 1.5, 1)
# #     plt.savefig(output_image, bbox_inches='tight', pad_inches=0.5)
# #     plt.close()
# #
# # # Example usage
# # audio_path =  r"C:\Users\zhangyuxuan\Desktop\wav\music_3.wav"  # Replace with the actual path to your audio
# # output_image =  r"C:\Users\zhangyuxuan\Desktop\wav\simplified_score.png"  # Path to save the generated image
# #
# # # Load the audio file
# # audio, sr = librosa.load(audio_path)
# #
# # # Detect notes and generate the score
# # notes = detect_notes(audio, sr)
# # plot_simplified_score(notes, output_image)
# #
# # print(f"Musical score saved to: {output_image}")
#
# import numpy as np
# import librosa
# import matplotlib.pyplot as plt
#
# # Map MIDI notes to numbered notation (1-7 for C major scale)
# NOTE_MAP = {'C': '1', 'D': '2', 'E': '3', 'F': '4', 'G': '5', 'A': '6', 'B': '7'}
#
#
# def detect_notes(audio, sr):
#     """Detect notes and their timestamps from the audio."""
#     pitches, magnitudes = librosa.piptrack(y=audio, sr=sr)
#     notes = []
#     for t in range(pitches.shape[1]):
#         index = magnitudes[:, t].argmax()
#         pitch = pitches[index, t]
#         if pitch > 0:
#             time = librosa.frames_to_time(t, sr=sr)
#             notes.append((pitch, time))
#     return notes
#
#
# def pitch_to_notation(pitch):
#     """Convert pitch (frequency in Hz) to numbered notation."""
#     note = librosa.hz_to_note(pitch)  # Get the note name (e.g., C4)
#     name, octave = note[:-1], int(note[-1])  # Split name and octave
#     number = NOTE_MAP.get(name, '?')  # Get numbered notation (1-7)
#
#     # Add dots for higher or lower octaves
#     if octave > 4:
#         return f"{number}·" * (octave - 4)  # Upper octave dot
#     elif octave < 4:
#         return f"·{number}" * (4 - octave)  # Lower octave dot
#     return number
#
#
# def plot_simplified_score(notes, output_image):
#     """Plot and save the numbered musical notation as an image."""
#     fig, ax = plt.subplots(figsize=(10, 6))
#     ax.axis('off')
#
#     # Set the number of notes per line
#     line_length = 8
#     lines = [notes[i:i + line_length] for i in range(0, len(notes), line_length)]
#
#     # Plot each line of notes
#     for i, line in enumerate(lines):
#         for j, (pitch, time) in enumerate(line):
#             notation = pitch_to_notation(pitch)
#             ax.text(j * 2, -i * 2, notation, fontsize=24, ha='center', va='center')
#
#     plt.xlim(-1, line_length * 2)
#     plt.ylim(-len(lines) * 2, 1)
#     plt.savefig(output_image, bbox_inches='tight', pad_inches=0.5)
#     plt.close()
#
#
# # # Example usage
# # audio_path = "/mnt/data/music_3.wav"  # Replace with your audio file path
# # output_image = "/mnt/data/simplified_score.png"  # Path to save the image
#
# audio_path =  r"C:\Users\zhangyuxuan\Desktop\wav\music_3.wav"  # Replace with the actual path to your audio
# output_image =  r"C:\Users\zhangyuxuan\Desktop\wav\simplified_score.png"  # Path to save the generated image
# # Load the audio and detect notes
# audio, sr = librosa.load(audio_path)
# notes = detect_notes(audio, sr)
#
# # Generate the musical notation image
# plot_simplified_score(notes, output_image)
#
# print(f"Musical score saved to: {output_image}")
#
import numpy as np
import librosa
import matplotlib.pyplot as plt

# Map MIDI notes to numbered notation (1-7 for C major scale)
NOTE_MAP = {'C': '1', 'D': '2', 'E': '3', 'F': '4', 'G': '5', 'A': '6', 'B': '7'}


def detect_notes(audio, sr):
    """Detect notes and their timestamps from the audio."""
    pitches, magnitudes = librosa.piptrack(y=audio, sr=sr)
    notes = []
    for t in range(pitches.shape[1]):
        index = magnitudes[:, t].argmax()
        pitch = pitches[index, t]
        if pitch > 0:
            time = librosa.frames_to_time(t, sr=sr)
            notes.append((pitch, time))
    return notes


def pitch_to_notation(pitch):
    """Convert pitch (frequency in Hz) to numbered notation."""
    note = librosa.hz_to_note(pitch)  # Get the note name (e.g., C4)
    name, octave = note[:-1], int(note[-1])  # Split name and octave
    number = NOTE_MAP.get(name, '?')  # Get numbered notation (1-7)

    # Add dots for higher or lower octaves
    if octave > 4:
        return f"{number}·" * (octave - 4)  # Upper octave dot
    elif octave < 4:
        return f"·{number}" * (4 - octave)  # Lower octave dot
    return number


def plot_simplified_score(notes, output_image):
    """Plot and save the numbered musical notation as an image."""
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('off')

    # Set the number of notes per line and spacing adjustments
    line_length = 8
    lines = [notes[i:i + line_length] for i in range(0, len(notes), line_length)]

    # Adjust spacing between notes and lines to prevent overlap
    x_spacing = 3  # Horizontal spacing between notes
    y_spacing = 2  # Vertical spacing between lines

    # Plot each line of notes
    for i, line in enumerate(lines):
        for j, (pitch, time) in enumerate(line):
            notation = pitch_to_notation(pitch)
            ax.text(j * x_spacing, -i * y_spacing, notation,
                    fontsize=20, ha='center', va='center')

    # Adjust plot limits to fit content properly
    plt.xlim(-1, line_length * x_spacing)
    plt.ylim(-len(lines) * y_spacing, 1)

    # Save the image without extra borders
    plt.savefig(output_image, bbox_inches='tight', pad_inches=0.1, dpi=300)
    plt.close()


# Example usage
# audio_path = "/mnt/data/music_3.wav"  # Replace with your audio file path
# output_image = "/mnt/data/simplified_score_fixed.png"  # Path to save the image
audio_path =  r"wav\music_1.wav"  # Replace with the actual path to your audio
output_image =  r"wav\simplified_score.png"  # Path to save the generated image
# Load the audio and detect notes
audio, sr = librosa.load(audio_path)
notes = detect_notes(audio, sr)

# Generate the musical notation image
plot_simplified_score(notes, output_image)

print(f"Musical score saved to: {output_image}")

