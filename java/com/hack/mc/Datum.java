package com.hack.mc;

public class Datum<E> {
	E e;

	public Datum(E e) {
		this.e = e;
	}

	public E getValue() {
		return e;
	}

	public String toString() {
		return e.toString();
	}
}
