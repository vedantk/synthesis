package com.hack.mc;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Scanner;

import javax.sound.midi.InvalidMidiDataException;
import javax.sound.midi.MidiEvent;
import javax.sound.midi.MidiSystem;
import javax.sound.midi.Sequence;
import javax.sound.midi.Track;

import com.hack.midi.MessageInfo;

public class MarkovChain<E> {
	private Map<Integer, Map<String, List<E>>> pMap;

	public MarkovChain() {
		pMap = new HashMap<Integer, Map<String, List<E>>>();
	}

	protected MarkovChain(Map<Integer, Map<String, List<E>>> data) {
		this.pMap = data;
	}

	public void train(List<E> data, int N) {
		for (int j = 0; j < N; j++) {
			Map<String, List<E>> foo = new HashMap<String, List<E>>();
			int n = j + 1;
			for (int i = 0; i < data.size(); i++) {
				int state = (i - n >= 0) ? (n - 1) : i;
				if (state == (n - 1)) {
					StringBuilder sb = new StringBuilder();
					for (int k = -state; k < 1; k++) {
						sb.append(data.get(i + k));
					}
					String d = sb.toString();
					if (i < data.size() - 1) {
						E e = data.get(i + 1);
						if (foo.containsKey(d)) {
							foo.get(d).add(e);
						} else {
							List<E> bar = new ArrayList<E>();
							bar.add(e);
							foo.put(d, bar);
						}
					}
				}
			}
			pMap.put(n, foo);
		}
	}

	public String generate(int length, int N) {
		StringBuilder sb = new StringBuilder();
		String cur = "";
		for (int i = 0; i < length; i++) {
			if (i == 0) {
				cur = selectRandomFromCollection(pMap.get(1).keySet())
						.toString();
			} else {
				int state = i < N ? i : N;
				while (true) {
					StringBuilder get = new StringBuilder();
					for (int j = -state; j < 0; j++) {
						get.append(sb.toString().charAt(i + j));
					}
					List<E> possibilities = pMap.get(state).get(get.toString());
					if (possibilities == null) {
						state--;

					} else {
						cur = selectRandomFromCollection(possibilities)
								.toString();
						break;
					}
				}
			}

			sb.append(cur);
		}
		return sb.toString();
	}

	public static void main(String[] args) {
		try {
			Sequence sequence = MidiSystem
					.getSequence(new File("cs1-1pre.mid"));
			Track[] tracks = sequence.getTracks();
			if (tracks != null) {
				// for (int i = 0; i < tracks.length; i++) {
				System.out.println("Track " + 0 + ":");
				Track track = tracks[0];
				for (int j = 0; j < track.size(); j++) {
					MidiEvent event = track.get(j);
					System.out.println(" tick " + event.getTick() + ", "
							+ MessageInfo.toString(event.getMessage()));
				} // for
					// } // for
			} // if
			System.out.println(sequence.getMicrosecondLength());
		} catch (InvalidMidiDataException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		} catch (IOException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		StringBuilder text = new StringBuilder();
		Scanner scanner = null;
		try {
			scanner = new Scanner(new FileInputStream("the_tempest.txt"));
			while (scanner.hasNextLine()) {
				text.append(scanner.nextLine() + "\n");
			}
			scanner.close();

		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		String test = text.toString().toLowerCase().replaceAll("\n", "");
		// String test = "markov chains are cool la";
		String ints = "12345679011";
		List<Character> data = new ArrayList<Character>();
		List<Integer> data2 = new ArrayList<Integer>();
		for (int i = 0; i < test.length(); i++) {
			data.add(new Character(test.charAt(i)));
		}
		for (int i = 0; i < ints.length(); i++) {
			data2.add(new Integer(Integer.parseInt(ints.charAt(i) + "")));
		}
		MarkovChain<Character> mc = new MarkovChain<Character>();
		mc.train(data, 10);
		System.out.println(mc.generate(100, 6));
	}

	public Object selectRandomFromCollection(Collection<?> set) {
		int size = set.size();
		int item = new Random().nextInt(size);
		int i = 0;
		for (Object c : set) {
			if (i == item)
				return c;
			i = i + 1;
		}
		return null;
	}

	public E selectRandomEFromCollection(Collection<E> set) {
		int size = set.size();
		int item = new Random().nextInt(size);
		int i = 0;
		for (E c : set) {
			if (i == item)
				return c;
			i = i + 1;
		}
		return null;
	}
}
