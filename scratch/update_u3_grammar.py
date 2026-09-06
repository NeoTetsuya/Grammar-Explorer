import sys
import io
import re
from bs4 import BeautifulSoup

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

CHART_3_1_HTML = """<div class="lg:col-span-5 bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-3">
  <div class="flex items-center justify-between border-b border-slate-100 pb-2">
    <h4 class="font-bold text-slate-900 text-sm sm:text-base">3.1 Spelling Rules for Plural Nouns</h4>
    <span class="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-mono">Page 62</span>
  </div>

  <div class="space-y-3 text-xs text-slate-700">
    <!-- Regular Plural Rules Table -->
    <div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm">
      <div class="bg-slate-100 px-3 py-1.5 font-bold text-slate-700 flex items-center justify-between">
        <span>Regular Plural Forms</span>
        <span class="text-[10px] text-slate-500 font-normal">Singular ➔ Plural</span>
      </div>
      <table class="w-full text-left text-slate-700">
        <tbody class="divide-y divide-slate-100">
          <tr>
            <td class="p-2 font-medium text-slate-600 bg-slate-50/50 w-2/5">Add -s to most nouns</td>
            <td class="p-2">apple ➔ <strong class="text-teal-700">apples</strong>, scientist ➔ <strong class="text-teal-700">scientists</strong>, boy ➔ <strong class="text-teal-700">boys</strong></td>
          </tr>
          <tr>
            <td class="p-2 font-medium text-slate-600 bg-slate-50/50">End in -s, -sh, -ch, -x (add -es)</td>
            <td class="p-2">class ➔ <strong class="text-teal-700">classes</strong>, dish ➔ <strong class="text-teal-700">dishes</strong>, inch ➔ <strong class="text-teal-700">inches</strong>, tax ➔ <strong class="text-teal-700">taxes</strong></td>
          </tr>
          <tr>
            <td class="p-2 font-medium text-slate-600 bg-slate-50/50">Consonant + -y (➔ -ies)</td>
            <td class="p-2">party ➔ <strong class="text-teal-700">parties</strong>, city ➔ <strong class="text-teal-700">cities</strong></td>
          </tr>
          <tr>
            <td class="p-2 font-medium text-slate-600 bg-slate-50/50">End in -o (add -s or -es)</td>
            <td class="p-2">photo ➔ <strong class="text-teal-700">photos</strong>, potato ➔ <strong class="text-teal-700">potatoes</strong></td>
          </tr>
          <tr>
            <td class="p-2 font-medium text-slate-600 bg-slate-50/50">End in -f / -fe (➔ -ves or -s)</td>
            <td class="p-2">leaf ➔ <strong class="text-teal-700">leaves</strong>, wife ➔ <strong class="text-teal-700">wives</strong> | belief ➔ <strong class="text-teal-700">beliefs</strong>, roof ➔ <strong class="text-teal-700">roofs</strong></td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Irregular Plural Categories -->
    <div class="border border-slate-200 rounded-xl p-3 bg-slate-50 space-y-1.5">
      <strong class="text-slate-800 block text-[11px] uppercase tracking-wide">Irregular Plural Nouns:</strong>
      <p>• <strong>Vowel change:</strong> man ➔ <strong class="text-amber-700">men</strong>, foot ➔ <strong class="text-amber-700">feet</strong>, tooth ➔ <strong class="text-amber-700">teeth</strong></p>
      <p>• <strong>Irregular ending:</strong> child ➔ <strong class="text-amber-700">children</strong>, person ➔ <strong class="text-amber-700">people</strong></p>
      <p>• <strong>No change (same singular &amp; plural):</strong> fish ➔ <strong class="text-teal-700">fish</strong>, deer ➔ <strong class="text-teal-700">deer</strong>, sheep ➔ <strong class="text-teal-700">sheep</strong></p>
      <p class="text-[11px] text-slate-500 pt-1 border-t border-slate-200 italic">See page A2 for a list of common irregular plural nouns.</p>
    </div>

    <!-- Real English: Plural-Only Nouns -->
    <div class="bg-amber-50/70 p-3 rounded-xl border border-amber-200 text-amber-950 space-y-1">
      <strong class="text-amber-900 block text-[11px] uppercase tracking-wide">Real English: Plural-Only Nouns</strong>
      <p>A few nouns have no singular form and are used only in the plural:</p>
      <p class="font-medium text-slate-800">• <em>clothes, glasses, jeans, scissors, pants</em></p>
      <p class="italic text-[11px] text-slate-600">e.g., I’m wearing my new jeans today.</p>
    </div>
  </div>
</div>"""

CHART_3_2_HTML = """<div class="lg:col-span-5 bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-3">
  <div class="flex items-center justify-between border-b border-slate-100 pb-2">
    <h4 class="font-bold text-slate-900 text-sm sm:text-base">3.2 Possessive Nouns</h4>
    <span class="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-mono">Page 63</span>
  </div>

  <div class="space-y-3 text-xs text-slate-700">
    <!-- Form Comparison Table -->
    <div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm">
      <div class="bg-slate-100 px-3 py-1.5 font-bold text-slate-700 flex items-center justify-between">
        <span>Possessive Forms</span>
        <span class="text-[10px] text-slate-500 font-normal">Noun ➔ Possessive</span>
      </div>
      <table class="w-full text-left text-slate-700">
        <tbody class="divide-y divide-slate-100">
          <tr>
            <td class="p-2 font-medium text-slate-600 bg-slate-50/50 w-2/5">Singular regular: girl</td>
            <td class="p-2">The <strong class="text-teal-700">girl’s</strong> bicycle is blue.</td>
          </tr>
          <tr>
            <td class="p-2 font-medium text-slate-600 bg-slate-50/50">Singular irregular: child</td>
            <td class="p-2">The <strong class="text-teal-700">child’s</strong> room is messy.</td>
          </tr>
          <tr>
            <td class="p-2 font-medium text-slate-600 bg-slate-50/50">Plural regular: girls</td>
            <td class="p-2">The <strong class="text-teal-700">girls’</strong> bicycles are blue.</td>
          </tr>
          <tr>
            <td class="p-2 font-medium text-slate-600 bg-slate-50/50">Plural irregular: children</td>
            <td class="p-2">The <strong class="text-teal-700">children’s</strong> rooms are messy.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Numbered Rules -->
    <div class="bg-slate-50 p-3 rounded-xl border border-slate-200 space-y-2 leading-relaxed">
      <div>
        <p><strong>1. Ownership or Relationship:</strong> Use possessive nouns to show who owns something or a relationship (<em>The writer’s house is in New York. / Mark’s father is very strong.</em>).</p>
      </div>
      <div class="pt-1.5 border-t border-slate-200">
        <p><strong>2. Singular Nouns:</strong> Add apostrophe + -s (<strong>’s</strong>) (<em>The child’s mother is over there.</em>).</p>
      </div>
      <div class="pt-1.5 border-t border-slate-200">
        <p><strong>3. Plural Nouns:</strong></p>
        <p class="text-slate-600">• Add apostrophe only (<strong>’</strong>) to regular plural nouns ending in -s: <em>The boys’ parents are here.</em></p>
        <p class="text-slate-600">• Add <strong>’s</strong> to irregular plural nouns not ending in -s: <em>The children’s teacher is kind.</em></p>
      </div>
      <div class="pt-1.5 border-t border-slate-200">
        <p><strong>4. Two or More Nouns:</strong> Add <strong>’s</strong> to the second noun only: <em>John and Tina’s father is sick.</em></p>
      </div>
    </div>
  </div>
</div>"""

CHART_3_3_HTML = """<div class="lg:col-span-5 bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-3">
  <div class="flex items-center justify-between border-b border-slate-100 pb-2">
    <h4 class="font-bold text-slate-900 text-sm sm:text-base">3.3 Another and Other</h4>
    <span class="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-mono">Page 64</span>
  </div>

  <div class="space-y-3 text-xs text-slate-700">
    <!-- Rules Breakdown -->
    <div class="bg-slate-50 p-3 rounded-xl border border-slate-200 space-y-2 leading-relaxed">
      <div>
        <span class="font-bold text-slate-800 block text-[11px] uppercase tracking-wide">1. Another + Singular Noun:</span>
        <p>• <strong>One more of the same group:</strong> <em>I’ve had two slices, but I’m going to have <strong>another</strong> piece.</em></p>
        <p>• <strong>A different person or thing:</strong> <em>This pen doesn’t work. I need <strong>another</strong> pen.</em></p>
        <p>• <strong>Not specific:</strong> <em>My car is old. I need to buy <strong>another</strong> car soon.</em></p>
      </div>

      <div class="pt-2 border-t border-slate-200">
        <span class="font-bold text-slate-800 block text-[11px] uppercase tracking-wide">2. The Other + Singular / Plural Noun:</span>
        <p>• <strong>The other + singular noun</strong> (the second of two in a specific group):<br><span class="text-slate-600"><em>There are two hotels. One is on Main St. <strong>The other hotel</strong> is on Oak St.</em></span></p>
        <p>• <strong>The other + plural noun</strong> (the rest of a specific group):<br><span class="text-slate-600"><em>We had three assignments. I finished one and did <strong>the other assignments</strong> today.</em></span></p>
      </div>

      <div class="pt-2 border-t border-slate-200">
        <span class="font-bold text-slate-800 block text-[11px] uppercase tracking-wide">3. Other + Plural Noun:</span>
        <p>• Means some, but not all, of the remaining people or things in a general group:<br><span class="text-slate-600"><em>Some people like to talk. <strong>Other people</strong> prefer to listen.</em></span></p>
      </div>

      <div class="pt-2 border-t border-slate-200">
        <span class="font-bold text-slate-800 block text-[11px] uppercase tracking-wide">4. Pronoun Replacement (One / Ones):</span>
        <p>• The pronoun <em>one</em> or <em>ones</em> can replace the noun:<br><span class="text-slate-600"><em>Lydia’s watch broke, so she bought <strong>another one</strong>.</em> (one = watch)<br><em>These earrings are pretty, but I prefer <strong>the other ones</strong>.</em> (ones = earrings)</span></p>
      </div>
    </div>

    <!-- Real English Pronoun Use -->
    <div class="bg-amber-50/70 p-3 rounded-xl border border-amber-200 text-amber-950 space-y-1">
      <strong class="text-amber-900 block text-[11px] uppercase tracking-wide">Real English: Used Alone as Pronouns</strong>
      <p><em>Another</em> and <em>the other</em> can also be used alone without a following noun:</p>
      <p>• <em>These pears are delicious. I’m going to have <strong>another</strong>.</em> (another = pear)</p>
      <p>• <em>Ken owns two apartments. One is in Chicago. <strong>The other</strong> is in Miami.</em> (the other = apartment)</p>
    </div>
  </div>
</div>"""

CHART_3_4_HTML = """<div class="lg:col-span-5 bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-3">
  <div class="flex items-center justify-between border-b border-slate-100 pb-2">
    <h4 class="font-bold text-slate-900 text-sm sm:text-base">3.4 Count Nouns &amp; Non-Count Nouns</h4>
    <span class="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-mono">Page 70</span>
  </div>

  <div class="space-y-3 text-xs text-slate-700">
    <!-- Comparison Table -->
    <div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm">
      <div class="bg-slate-100 px-3 py-1.5 font-bold text-slate-700 flex items-center justify-between">
        <span>Noun Comparison</span>
        <span class="text-[10px] text-slate-500 font-normal">Count vs. Non-Count</span>
      </div>
      <table class="w-full text-left text-slate-700">
        <tbody class="divide-y divide-slate-100">
          <tr>
            <td class="p-2.5 font-medium text-slate-600 bg-slate-50/50 w-1/3">Count Nouns</td>
            <td class="p-2.5">
              <p>• Have singular and plural forms (<em>banana / bananas, doctor / doctors</em>).</p>
              <p>• Singular count nouns <strong>must have</strong> <em>a, an,</em> or another determiner (<em>an apple, the doctor</em>).</p>
              <p>• Plural count nouns take plural verbs (<em>Apples are sweet.</em>).</p>
            </td>
          </tr>
          <tr>
            <td class="p-2.5 font-medium text-slate-600 bg-slate-50/50">Non-Count Nouns</td>
            <td class="p-2.5">
              <p>• Name things that cannot be counted separately (<em>water, air, advice, rice</em>).</p>
              <p>• Do <strong>not</strong> have plural forms (no -s).</p>
              <p>• Do <strong>not</strong> use <em>a</em> or <em>an</em>.</p>
              <p>• Always take <strong>singular verbs</strong> (<em>Water is essential.</em>).</p>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Dual Meaning Real English -->
    <div class="bg-amber-50/80 p-3 rounded-xl border border-amber-200 text-amber-950 space-y-1.5">
      <strong class="text-amber-900 block text-[11px] uppercase tracking-wide">Real English: Count and Non-Count with Different Meanings</strong>
      <p>Some nouns can be count with one meaning and non-count with another:</p>
      <div class="space-y-1 pt-1 text-slate-800">
        <p>• <strong>time:</strong> <em>She goes to the gym three <strong>times</strong> a week.</em> (count = occasions)<br><span class="text-slate-600">vs. <em>I don’t have <strong>time</strong> to go to the gym today.</em> (non-count = general time)</span></p>
        <p>• <strong>exercise:</strong> <em>We had three <strong>exercises</strong> for homework.</em> (count = specific tasks)<br><span class="text-slate-600">vs. <em><strong>Exercise</strong> is important for good health.</em> (non-count = physical activity)</span></p>
        <p>• <strong>experience:</strong> <em>She had many interesting <strong>experiences</strong>.</em> (count = events)<br><span class="text-slate-600">vs. <em>He has five years of <strong>experience</strong>.</em> (non-count = knowledge/skill)</span></p>
      </div>
    </div>
  </div>
</div>"""

CHART_3_5_HTML = """<div class="lg:col-span-5 bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-3">
  <div class="flex items-center justify-between border-b border-slate-100 pb-2">
    <h4 class="font-bold text-slate-900 text-sm sm:text-base">3.5 Categories of Non-Count Nouns</h4>
    <span class="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-mono">Page 71</span>
  </div>

  <div class="space-y-2 text-xs text-slate-700">
    <!-- 4 Structured Boxes -->
    <div class="p-2.5 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
      <span class="font-bold text-slate-800 block text-[11px] uppercase tracking-wide">1. Category of Related Items:</span>
      <p class="text-slate-600">The general category noun is non-count; specific items in it are count:</p>
      <p class="font-medium text-teal-800">• <strong>clothing</strong> (pants, sweaters, shoes) | <strong>fruit</strong> (apples, bananas) | <strong>furniture</strong> (tables, chairs) | <strong>homework</strong> (assignments) | <strong>jewelry</strong> (rings, necklaces) | <strong>money</strong> (coins, dollars) | <strong>mail</strong> (letters, packages) | <strong>weather</strong> (storms, rain)</p>
    </div>

    <div class="p-2.5 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
      <span class="font-bold text-slate-800 block text-[11px] uppercase tracking-wide">2. Mass / Substances / Fluids (No Separate Parts):</span>
      <p class="font-medium text-slate-800">• <em>air, cheese, coffee, fish, flour, hair, ice, juice, meat, milk, oil, rice, skin, soup, sugar, tea, water, wind</em></p>
    </div>

    <div class="p-2.5 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
      <span class="font-bold text-slate-800 block text-[11px] uppercase tracking-wide">3. Abstract Nouns (Ideas, Feelings, Qualities):</span>
      <p class="font-medium text-slate-800">• <em>advice, beauty, energy, experience, fun, happiness, health, help, honesty, intelligence, knowledge, love, nature, work</em></p>
    </div>

    <div class="p-2.5 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
      <span class="font-bold text-slate-800 block text-[11px] uppercase tracking-wide">4. Subjects of Study:</span>
      <p class="font-medium text-slate-800">• <em>biology, chemistry, geometry, history, math, physics, science</em></p>
    </div>
  </div>
</div>"""

CHART_3_6_HTML = """<div class="lg:col-span-5 bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-3">
  <div class="flex items-center justify-between border-b border-slate-100 pb-2">
    <h4 class="font-bold text-slate-900 text-sm sm:text-base">3.6 Quantity Words Summary</h4>
    <span class="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-mono">Page 76</span>
  </div>

  <div class="space-y-2.5 text-xs text-slate-700">
    <!-- 5 Rules Breakdown -->
    <div class="bg-slate-50 p-3 rounded-xl border border-slate-200 space-y-2 leading-relaxed">
      <div>
        <p><strong>1. some:</strong> Use with count and non-count nouns in affirmative statements:</p>
        <p class="text-slate-600">• <em>We need <strong>some</strong> bananas.</em> | <em>I left <strong>some</strong> fruit on the table.</em></p>
      </div>

      <div class="pt-1.5 border-t border-slate-200">
        <p><strong>2. any:</strong> Use with count and non-count nouns in negative statements and questions:</p>
        <p class="text-slate-600">• <em>Maria doesn’t want <strong>any</strong> oranges.</em> | <em>I don’t have <strong>any</strong> homework.</em></p>
      </div>

      <div class="pt-1.5 border-t border-slate-200">
        <p><strong>3. a few / many:</strong> Use with <strong>count nouns</strong> only:</p>
        <p class="text-slate-600">• <em>I have <strong>a few</strong> questions.</em> | <em>Did you buy <strong>many</strong> apples?</em></p>
      </div>

      <div class="pt-1.5 border-t border-slate-200">
        <p><strong>4. a little / much:</strong> Use with <strong>non-count nouns</strong> only:</p>
        <p class="text-slate-600">• <em>Give the plants <strong>a little</strong> water.</em> | <em>We don’t have <strong>much</strong> homework tonight.</em></p>
      </div>

      <div class="pt-1.5 border-t border-slate-200">
        <p><strong>5. a lot of:</strong> Use with <strong>both</strong> count and non-count nouns:</p>
        <p class="text-slate-600">• <em>We bought <strong>a lot of</strong> vegetables.</em> | <em>She eats <strong>a lot of</strong> sugar.</em></p>
      </div>
    </div>
  </div>
</div>"""

CHART_3_7_HTML = """<div class="lg:col-span-5 bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-3">
  <div class="flex items-center justify-between border-b border-slate-100 pb-2">
    <h4 class="font-bold text-slate-900 text-sm sm:text-base">3.7 Measurement Words with Non-Count Nouns</h4>
    <span class="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-mono">Page 77</span>
  </div>

  <div class="space-y-3 text-xs text-slate-700">
    <!-- 5 Categories Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
      <div class="p-2 bg-slate-50 rounded-lg border border-slate-200">
        <strong class="text-slate-800 block text-[11px] uppercase mb-0.5">Containers</strong>
        <p class="text-slate-600"><em>a bag of rice, a bottle of juice, a bowl of cereal, a box of cereal, a can of soda, a carton of milk, a cup of coffee, a glass of water, a jar of jam</em></p>
      </div>
      <div class="p-2 bg-slate-50 rounded-lg border border-slate-200">
        <strong class="text-slate-800 block text-[11px] uppercase mb-0.5">Units / Measurements</strong>
        <p class="text-slate-600"><em>a gallon of milk, a pint of ice cream, a pound of meat, a quart of oil, a tablespoon of sugar, a teaspoon of salt</em></p>
      </div>
      <div class="p-2 bg-slate-50 rounded-lg border border-slate-200">
        <strong class="text-slate-800 block text-[11px] uppercase mb-0.5">Portions</strong>
        <p class="text-slate-600"><em>a piece of cake, a piece of pie, a slice of bread, a slice of pizza</em></p>
      </div>
      <div class="p-2 bg-slate-50 rounded-lg border border-slate-200">
        <strong class="text-slate-800 block text-[11px] uppercase mb-0.5">Shapes &amp; Other</strong>
        <p class="text-slate-600"><em>a bar of chocolate/soap, a loaf of bread, a sheet of paper, a stick of butter, a tube of toothpaste | a piece of jewelry/mail</em></p>
      </div>
    </div>

    <!-- Rules & Warning -->
    <div class="bg-amber-50/80 p-3 rounded-xl border border-amber-200 text-amber-950 space-y-1.5">
      <p><strong>Rule:</strong> Use a measurement word + <strong>of</strong> to talk about a specific quantity of a non-count noun (<em>He drank a bottle of juice. / I bought three loaves of bread.</em>).</p>
      <div class="pt-1.5 border-t border-amber-200 text-rose-700 font-semibold">
        ⚠️ <strong>Be careful!</strong> Do NOT use a number directly before a non-count noun!
      </div>
      <p class="font-mono text-[11px] text-emerald-800">✓ Put two bars of soap in the bathroom.</p>
      <p class="font-mono text-[11px] text-rose-600">✗ Put two soap in the bathroom.</p>
    </div>
  </div>
</div>"""

GRAMMAR_FOCUS_HTML = """<div class="bg-teal-50 rounded-xl border border-teal-200 p-4 text-xs text-teal-950 space-y-1.5">
  <span class="font-bold text-teal-900 block text-xs uppercase tracking-wide">GRAMMAR FOCUS: Count &amp; Non-Count Nouns with Modifiers (Page 84)</span>
  <p class="text-slate-700">In the model text, the writer uses singular and plural count nouns and non-count nouns with and without adjectives and quantity words:</p>
  <div class="space-y-1.5 text-slate-800 font-medium pl-2 border-l-2 border-teal-500 mt-1">
    <p>• <strong>Count Nouns:</strong><br><span class="text-slate-600 italic">Singular with a/an: to take a long walk • Plural: comfortable shoes • Quantity word: any fancy machines</span></p>
    <p>• <strong>Non-Count Nouns:</strong><br><span class="text-slate-600 italic">(No a/an): Exercise is important • Quantity word: a lot of expensive clothing, very little time and money</span></p>
  </div>
</div>"""

def find_chart_card(soup, prefix):
    for c in soup.select('.reader-card'):
        h = c.find(['h2', 'h3', 'h4', 'h5'])
        if h and prefix in h.get_text():
            return c
    return None

def update_u3_all_in_one():
    fpath = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 3/GE2 - U3.html'
    soup = BeautifulSoup(open(fpath, encoding='utf-8'), 'html.parser')

    # 3.1
    c31 = find_chart_card(soup, '3.1')
    if c31:
        new_tag = BeautifulSoup(CHART_3_1_HTML, 'html.parser').find(class_='reader-card')
        c31.replace_with(new_tag)
        print("  + Replaced Chart 3.1 in GE2 - U3.html")

    # 3.2
    c32 = find_chart_card(soup, '3.2')
    if c32:
        new_tag = BeautifulSoup(CHART_3_2_HTML, 'html.parser').find(class_='reader-card')
        c32.replace_with(new_tag)
        print("  + Replaced Chart 3.2 in GE2 - U3.html")

    # 3.3: Insert before Exercise 9
    c33_exist = find_chart_card(soup, '3.3')
    new_c33 = BeautifulSoup(CHART_3_3_HTML, 'html.parser').find(class_='reader-card')
    if c33_exist:
        c33_exist.replace_with(new_c33)
        print("  + Replaced Chart 3.3 in GE2 - U3.html")
    else:
        # Locate Exercise 9
        for c in soup.select('#tab-lesson1 .reader-card'):
            if 'Another, Other' in c.get_text():
                # Check parent
                if 'lg:col-span-6' in c.get('class', []):
                    c['class'] = [cl for cl in c.get('class', []) if cl != 'lg:col-span-6'] + ['lg:col-span-7']
                    new_c33['class'] = [cl for cl in new_c33.get('class', []) if cl != 'lg:col-span-5'] + ['lg:col-span-5']
                c.insert_before(new_c33)
                print("  + Inserted Chart 3.3 before Exercise 9 in GE2 - U3.html")
                break

    # 3.4
    c34 = find_chart_card(soup, '3.4')
    if c34:
        new_tag = BeautifulSoup(CHART_3_4_HTML, 'html.parser').find(class_='reader-card')
        c34.replace_with(new_tag)
        print("  + Replaced Chart 3.4 in GE2 - U3.html")

    # 3.5
    c35 = find_chart_card(soup, '3.5')
    if c35:
        new_tag = BeautifulSoup(CHART_3_5_HTML, 'html.parser').find(class_='reader-card')
        c35.replace_with(new_tag)
        print("  + Replaced Chart 3.5 in GE2 - U3.html")

    # 3.6
    c36 = find_chart_card(soup, '3.6')
    if c36:
        new_tag = BeautifulSoup(CHART_3_6_HTML, 'html.parser').find(class_='reader-card')
        c36.replace_with(new_tag)
        print("  + Replaced Chart 3.6 in GE2 - U3.html")

    # 3.7: Insert before Exercise 5 (Measurement Words)
    c37_exist = find_chart_card(soup, '3.7')
    new_c37 = BeautifulSoup(CHART_3_7_HTML, 'html.parser').find(class_='reader-card')
    if c37_exist:
        c37_exist.replace_with(new_c37)
        print("  + Replaced Chart 3.7 in GE2 - U3.html")
    else:
        for c in soup.select('#tab-lesson3 .reader-card'):
            if 'Measurement Words' in c.get_text():
                # If c is inside a grid, let's make sure it's cleanly paired
                c.insert_before(new_c37)
                print("  + Inserted Chart 3.7 before Exercise 5 in GE2 - U3.html")
                break

    # Grammar Focus in Model Reading (tab-writing)
    for c in soup.select('#tab-writing .reader-card'):
        if 'Staying Fit' in c.get_text():
            if not c.find(string=re.compile('GRAMMAR FOCUS')):
                writing_focus = c.find(string=re.compile('WRITING FOCUS'))
                gf_tag = BeautifulSoup(GRAMMAR_FOCUS_HTML, 'html.parser')
                if writing_focus:
                    wf_box = writing_focus.find_parent(class_=lambda x: x and 'rounded-xl' in x)
                    if wf_box:
                        wf_box.insert_before(gf_tag)
                    else:
                        c.append(gf_tag)
                else:
                    c.append(gf_tag)
                print("  + Added GRAMMAR FOCUS to Model Reading in GE2 - U3.html")
            break

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("[SUCCESS] GE2 - U3.html updated!")

def update_u3_lesson_1():
    fpath = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 3/grammar_explorer_2_unit_3_lesson_1.html'
    soup = BeautifulSoup(open(fpath, encoding='utf-8'), 'html.parser')

    c31 = find_chart_card(soup, '3.1')
    if c31:
        new_tag = BeautifulSoup(CHART_3_1_HTML, 'html.parser').find(class_='reader-card')
        c31.replace_with(new_tag)
        print("  + Replaced Chart 3.1 in grammar_explorer_2_unit_3_lesson_1.html")

    c32 = find_chart_card(soup, '3.2')
    if c32:
        new_tag = BeautifulSoup(CHART_3_2_HTML, 'html.parser').find(class_='reader-card')
        c32.replace_with(new_tag)
        print("  + Replaced Chart 3.2 in grammar_explorer_2_unit_3_lesson_1.html")

    c33_exist = find_chart_card(soup, '3.3')
    new_c33 = BeautifulSoup(CHART_3_3_HTML, 'html.parser').find(class_='reader-card')
    if c33_exist:
        c33_exist.replace_with(new_c33)
        print("  + Replaced Chart 3.3 in grammar_explorer_2_unit_3_lesson_1.html")
    else:
        for c in soup.select('.reader-card'):
            if 'Another, Other' in c.get_text():
                c.insert_before(new_c33)
                print("  + Inserted Chart 3.3 before Exercise 9 in grammar_explorer_2_unit_3_lesson_1.html")
                break

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("[SUCCESS] grammar_explorer_2_unit_3_lesson_1.html updated!")

def update_u3_lesson_2():
    fpath = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 3/grammar_explorer_2_unit_3_lesson_2.html'
    soup = BeautifulSoup(open(fpath, encoding='utf-8'), 'html.parser')

    c34 = find_chart_card(soup, '3.4')
    if c34:
        new_tag = BeautifulSoup(CHART_3_4_HTML, 'html.parser').find(class_='reader-card')
        c34.replace_with(new_tag)
        print("  + Replaced Chart 3.4 in grammar_explorer_2_unit_3_lesson_2.html")

    c35 = find_chart_card(soup, '3.5')
    if c35:
        new_tag = BeautifulSoup(CHART_3_5_HTML, 'html.parser').find(class_='reader-card')
        c35.replace_with(new_tag)
        print("  + Replaced Chart 3.5 in grammar_explorer_2_unit_3_lesson_2.html")

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("[SUCCESS] grammar_explorer_2_unit_3_lesson_2.html updated!")

def update_u3_lesson_3():
    fpath = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 3/grammar_explorer_2_unit_3_lesson_3.html'
    soup = BeautifulSoup(open(fpath, encoding='utf-8'), 'html.parser')

    c36 = find_chart_card(soup, '3.6')
    if c36:
        new_tag = BeautifulSoup(CHART_3_6_HTML, 'html.parser').find(class_='reader-card')
        c36.replace_with(new_tag)
        print("  + Replaced Chart 3.6 in grammar_explorer_2_unit_3_lesson_3.html")

    c37_exist = find_chart_card(soup, '3.7')
    new_c37 = BeautifulSoup(CHART_3_7_HTML, 'html.parser').find(class_='reader-card')
    if c37_exist:
        c37_exist.replace_with(new_c37)
        print("  + Replaced Chart 3.7 in grammar_explorer_2_unit_3_lesson_3.html")
    else:
        for c in soup.select('.reader-card'):
            if 'Measurement Words' in c.get_text():
                c.insert_before(new_c37)
                print("  + Inserted Chart 3.7 before Exercise 5 in grammar_explorer_2_unit_3_lesson_3.html")
                break

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("[SUCCESS] grammar_explorer_2_unit_3_lesson_3.html updated!")

def update_u3_review_writing():
    fpath = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 3/grammar_explorer_2_unit_3_review_writing.html'
    soup = BeautifulSoup(open(fpath, encoding='utf-8'), 'html.parser')

    for c in soup.select('.reader-card'):
        if 'Staying Fit' in c.get_text():
            if not c.find(string=re.compile('GRAMMAR FOCUS')):
                writing_focus = c.find(string=re.compile('WRITING FOCUS'))
                gf_tag = BeautifulSoup(GRAMMAR_FOCUS_HTML, 'html.parser')
                if writing_focus:
                    wf_box = writing_focus.find_parent(class_=lambda x: x and 'rounded-xl' in x)
                    if wf_box:
                        wf_box.insert_before(gf_tag)
                    else:
                        c.append(gf_tag)
                else:
                    c.append(gf_tag)
                print("  + Added GRAMMAR FOCUS to Model Reading in grammar_explorer_2_unit_3_review_writing.html")
            break

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("[SUCCESS] grammar_explorer_2_unit_3_review_writing.html updated!")

if __name__ == '__main__':
    print("Executing Unit 3 Grammar Content Updates...")
    update_u3_all_in_one()
    update_u3_lesson_1()
    update_u3_lesson_2()
    update_u3_lesson_3()
    update_u3_review_writing()
    print("All Unit 3 grammar updates completed!")
