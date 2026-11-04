class StringComparableTest implements ComparableContract<String> {

    @Override
    public String createSmallerValue() {
        return "apple";
    }

    @Override
    public String createLargerValue() {
        return "banana";
    }
}
