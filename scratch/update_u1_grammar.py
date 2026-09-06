import sys
import io
import re
from bs4 import BeautifulSoup

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

CHART_1_1_HTML = """<div class="lg:col-span-5 bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-3">
  <div class="flex items-center justify-between border-b border-slate-100 pb-2">
    <h4 class="font-bold text-slate-900 text-sm sm:text-base">1.1 Simple Present: Affirmative & Negative Statements</h4>
    <span class="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-mono">Page 6</span>
  </div>

  <div class="space-y-3 text-xs">
    <!-- Affirmative Table -->
    <div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm">
      <div class="bg-slate-100 px-3 py-1.5 font-bold text-slate-700 flex items-center justify-between">
        <span>Affirmative Statements</span>
        <span class="text-[10px] text-slate-500 font-normal">Subject + Verb</span>
      </div>
      <table class="w-full text-left">
        <tbody class="divide-y divide-slate-100 text-slate-700">
          <tr>
            <td class="p-2.5 font-medium text-slate-600 bg-slate-50/50 w-1/2">I / You / We / They</td>
            <td class="p-2.5 font-semibold text-slate-900"><span class="text-teal-700">eat</span> a lot.</td>
          </tr>
          <tr>
            <td class="p-2.5 font-medium text-slate-600 bg-slate-50/50">He / She / It</td>
            <td class="p-2.5 font-semibold text-slate-900"><span class="text-amber-600">eats</span> a lot.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Negative Table -->
    <div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm">
      <div class="bg-slate-100 px-3 py-1.5 font-bold text-slate-700 flex items-center justify-between">
        <span>Negative Statements</span>
        <span class="text-[10px] text-slate-500 font-normal">Subject + Do/Does Not + Base Form</span>
      </div>
      <table class="w-full text-left">
        <tbody class="divide-y divide-slate-100 text-slate-700">
          <tr>
            <td class="p-2.5 font-medium text-slate-600 bg-slate-50/50 w-1/2">I / You / We / They</td>
            <td class="p-2.5 font-semibold text-slate-900"><span class="text-rose-600">do not / don’t</span> eat a lot.</td>
          </tr>
          <tr>
            <td class="p-2.5 font-medium text-slate-600 bg-slate-50/50">He / She / It</td>
            <td class="p-2.5 font-semibold text-slate-900"><span class="text-rose-600">does not / doesn’t</span> eat a lot.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Contractions note -->
    <div class="p-2.5 bg-slate-50 rounded-xl border border-slate-200 text-slate-700">
      <span class="font-bold text-slate-800">Contractions:</span> Usually used in conversation and informal writing (<em class="text-slate-900">He doesn’t watch TV. We don’t like pizza.</em>).
    </div>

    <!-- Uses -->
    <div class="bg-slate-50 p-3 rounded-xl border border-slate-200 space-y-1.5 leading-relaxed text-slate-700">
      <span class="font-bold text-slate-800 block text-[11px] uppercase tracking-wide">Use the Simple Present to talk about:</span>
      <p>• <strong>Habits and repeated actions:</strong> <em>We eat dinner at 7:30.</em></p>
      <p>• <strong>Facts and general truths:</strong> <em>The mail doesn't come on Sundays.</em></p>
      <p>• <strong>How often something happens:</strong> <em>Jim visits his uncle twice a year.</em></p>
    </div>

    <!-- Be Careful & Spelling -->
    <div class="bg-amber-50/80 p-3 rounded-xl border border-amber-200 text-amber-950 space-y-1.5">
      <div class="flex items-center gap-1.5 font-bold text-amber-900">
        <svg class="w-4 h-4 text-amber-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/></svg>
        <span>Be Careful! 3rd-Person Singular Endings</span>
      </div>
      <p>Don’t forget to add <strong>-s, -es,</strong> or <strong>-ies</strong> to verbs when the subject is <em>he, she, it,</em> or a singular noun.</p>
      <p class="font-mono text-[11px] text-emerald-800">✓ Rosa teaches math.</p>
      <p class="font-mono text-[11px] text-rose-600">✗ Rosa teach math.</p>
      <p class="text-[11px] text-slate-500 pt-1 border-t border-amber-200/60 italic">See page A1 for simple present spelling rules (-s, -es, -ies).</p>
    </div>
  </div>
</div>"""

CHART_1_2_HTML = """<div class="lg:col-span-5 bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-3">
  <div class="flex items-center justify-between border-b border-slate-100 pb-2">
    <h4 class="font-bold text-slate-900 text-sm sm:text-base">1.2 Simple Present: Questions and Answers</h4>
    <span class="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-mono">Page 7</span>
  </div>

  <div class="space-y-3 text-xs">
    <!-- Yes/No Questions Table -->
    <div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm">
      <div class="bg-slate-100 px-3 py-1.5 font-bold text-slate-700 flex items-center justify-between">
        <span>Yes / No Questions</span>
        <span class="text-[10px] text-slate-500 font-normal">Short Answers</span>
      </div>
      <div class="p-2.5 bg-white space-y-2 text-slate-700">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-1 border-b border-slate-100 pb-1.5">
          <span><strong>Do</strong> I / you / we / they <strong>sing</strong>?</span>
          <span class="text-slate-600 font-medium">→ <em>Yes, I do. / No, I don’t.</em></span>
        </div>
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-1">
          <span><strong>Does</strong> he / she / it <strong>sing</strong>?</span>
          <span class="text-slate-600 font-medium">→ <em>Yes, he does. / No, he doesn’t.</em></span>
        </div>
      </div>
    </div>

    <!-- Wh- Questions Table -->
    <div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm">
      <div class="bg-slate-100 px-3 py-1.5 font-bold text-slate-700 flex items-center justify-between">
        <span>Wh- Questions (Information)</span>
        <span class="text-[10px] text-slate-500 font-normal">Wh- + Do/Does + S + Verb</span>
      </div>
      <div class="p-2.5 bg-white space-y-1.5 text-slate-700">
        <p>• <strong>What do</strong> I sing? → <em class="text-slate-900 font-medium">Popular songs.</em></p>
        <p>• <strong>When do</strong> you sing? → <em class="text-slate-900 font-medium">Every Saturday night.</em></p>
        <p>• <strong>Why do</strong> they sing? → <em class="text-slate-900 font-medium">They love music.</em></p>
        <p>• <strong>Who does</strong> she visit? → <em class="text-slate-900 font-medium">Her father.</em></p>
        <p>• <strong>How often does</strong> she visit? → <em class="text-slate-900 font-medium">Twice a year.</em></p>
        <p>• <strong>How does</strong> he celebrate? → <em class="text-slate-900 font-medium">He has a party.</em></p>
      </div>
    </div>

    <!-- Who / What as Subject -->
    <div class="border border-amber-200 rounded-xl overflow-hidden bg-amber-50/60 shadow-sm">
      <div class="bg-amber-100/80 px-3 py-1.5 font-bold text-amber-900 flex items-center justify-between">
        <span>Who or What as Subject</span>
        <span class="text-[10px] text-amber-800 font-normal">Who/What + Verb (-s/-es)</span>
      </div>
      <div class="p-2.5 space-y-1.5 text-slate-800">
        <div class="flex items-center justify-between">
          <span>• <strong>Who teaches</strong> this class?</span>
          <span class="text-slate-600 font-medium">→ <em>Professor Ortega.</em></span>
        </div>
        <div class="flex items-center justify-between">
          <span>• <strong>What makes</strong> you happy?</span>
          <span class="text-slate-600 font-medium">→ <em>My family.</em></span>
        </div>
        <div class="mt-2 pt-2 border-t border-amber-200 text-rose-600 text-[11px] font-semibold flex items-center gap-1.5">
          <span>⚠️ <strong>Be careful!</strong> Do NOT use <em>do</em> or <em>does</em> when Who/What is subject!</span>
        </div>
        <div class="text-[11px] space-y-0.5">
          <p class="text-emerald-800 font-mono">✓ Who teaches this class?</p>
          <p class="text-rose-600 font-mono">✗ Who does teach this class?</p>
        </div>
      </div>
    </div>

    <!-- Explanations & Rules -->
    <div class="bg-slate-50 p-3 rounded-xl border border-slate-200 space-y-1.5 text-slate-700">
      <span class="font-bold text-slate-800 block text-[11px] uppercase tracking-wide">Key Rules:</span>
      <p><strong>1. Yes/No questions:</strong> Ask for answers of yes or no (<em>A: Do you speak Russian? B: Yes, I do. / No, I don’t.</em>).</p>
      <p><strong>2. Wh- questions:</strong> Ask for specific information (person, place, thing, reason, frequency) (<em>A: Where does Jeff live? B: In Sydney.</em>).</p>
      <p><strong>3. Who/What as subject:</strong> The verb is always in the 3rd person singular form (-s/-es) (<em>A: Who teaches math? B: Arlene.</em>).</p>
    </div>
  </div>
</div>"""

CHART_1_3_HTML = """<div class="lg:col-span-5 bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-3">
  <div class="flex items-center justify-between border-b border-slate-100 pb-2">
    <h4 class="font-bold text-slate-900 text-sm sm:text-base">1.3 Frequency Adverbs with Simple Present</h4>
    <span class="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-mono">Page 8</span>
  </div>

  <!-- Spectrum Bar -->
  <div class="p-3 bg-gradient-to-r from-teal-500 via-amber-400 to-rose-500 rounded-xl text-white font-bold text-[10px] sm:text-[11px] flex items-center justify-between shadow-sm">
    <span>100% Always</span>
    <span>Usually</span>
    <span>Often</span>
    <span>Sometimes</span>
    <span>Rarely/Seldom</span>
    <span>0% Never</span>
  </div>

  <div class="space-y-2.5 text-xs text-slate-700">
    <!-- Word Bank Badge List -->
    <div class="p-2.5 bg-slate-50 rounded-xl border border-slate-200">
      <span class="font-bold text-slate-800 block mb-1 text-[11px] uppercase tracking-wide">Common Frequency Adverbs:</span>
      <div class="flex flex-wrap gap-1.5">
        <span class="px-2 py-0.5 bg-white border border-slate-200 rounded font-semibold text-slate-800 text-[11px]">always</span>
        <span class="px-2 py-0.5 bg-white border border-slate-200 rounded font-semibold text-slate-800 text-[11px]">usually</span>
        <span class="px-2 py-0.5 bg-white border border-slate-200 rounded font-semibold text-slate-800 text-[11px]">often / frequently</span>
        <span class="px-2 py-0.5 bg-white border border-slate-200 rounded font-semibold text-slate-800 text-[11px]">sometimes</span>
        <span class="px-2 py-0.5 bg-white border border-slate-200 rounded font-semibold text-slate-800 text-[11px]">rarely / seldom / hardly ever</span>
        <span class="px-2 py-0.5 bg-white border border-slate-200 rounded font-semibold text-slate-800 text-[11px]">never</span>
      </div>
    </div>

    <!-- Position Rules -->
    <div class="bg-slate-50 p-3 rounded-xl border border-slate-200 space-y-2 leading-relaxed">
      <div>
        <p class="font-bold text-slate-800">1. Tell How Often Something Happens:</p>
        <p class="text-slate-600">• <em>I usually enjoy parties.</em></p>
        <p class="text-slate-600">• <em>I don’t always remember his birthday.</em></p>
        <p class="text-slate-600">• <em>Do you sometimes eat at restaurants?</em></p>
      </div>

      <div class="pt-2 border-t border-slate-200">
        <p class="font-bold text-slate-800">2. Position with 'be' vs. Other Verbs:</p>
        <p class="text-slate-600">• <strong>After 'be':</strong> <em>I am <strong>sometimes</strong> early for class.</em> | <em>Jenny isn’t <strong>often</strong> late.</em> | <em>Wedding guests are <strong>usually</strong> happy.</em></p>
        <p class="text-slate-600">• <strong>Before other verbs:</strong> <em>I <strong>usually</strong> enjoy parties.</em> | <em>He <strong>hardly ever</strong> stays home.</em></p>
      </div>

      <div class="pt-2 border-t border-slate-200">
        <p class="font-bold text-slate-800">3. Beginning or End of Sentence:</p>
        <p class="text-slate-600"><em>Sometimes, usually, frequently,</em> or <em>often</em> can also come at the beginning or end of a statement:</p>
        <p class="text-slate-600">• <em>Brides wear red dresses <strong>sometimes</strong>.</em></p>
        <p class="text-slate-600">• <em><strong>Usually</strong> Western brides wear white.</em></p>
      </div>

      <div class="pt-2 border-t border-slate-200 bg-amber-50/60 -mx-3 -mb-3 p-3 rounded-b-xl border-amber-200 text-amber-950">
        <p class="font-bold text-amber-900">4. Using 'Ever' in Questions:</p>
        <p class="text-slate-700"><em>Ever</em> is common in questions about frequency (means <em>at any time</em>). It is not usually used in affirmative statements:</p>
        <p class="text-slate-700 mt-1">• A: <em>Do you <strong>ever</strong> eat at restaurants?</em></p>
        <p class="text-slate-700">• B: <em>No, I <strong>never</strong> do. / Yes, I <strong>often</strong> do.</em></p>
      </div>
    </div>
  </div>
</div>"""

CHART_1_4_HTML = """<div class="lg:col-span-5 bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-3">
  <div class="flex items-center justify-between border-b border-slate-100 pb-2">
    <h4 class="font-bold text-slate-900 text-sm sm:text-base">1.4 Present Progressive: Statements</h4>
    <span class="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-mono">Page 14</span>
  </div>

  <div class="space-y-3 text-xs">
    <!-- Affirmative Table -->
    <div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm">
      <div class="bg-slate-100 px-3 py-1.5 font-bold text-slate-700 flex items-center justify-between">
        <span>Affirmative Statements</span>
        <span class="text-[10px] text-slate-500 font-normal">Subject + Be + Verb-ing</span>
      </div>
      <table class="w-full text-left">
        <tbody class="divide-y divide-slate-100 text-slate-700">
          <tr>
            <td class="p-2 font-medium text-slate-600 bg-slate-50/50 w-2/5">I</td>
            <td class="p-2 font-semibold text-slate-900"><span class="text-teal-700">am / ’m</span> studying.</td>
          </tr>
          <tr>
            <td class="p-2 font-medium text-slate-600 bg-slate-50/50">He / She / It</td>
            <td class="p-2 font-semibold text-slate-900"><span class="text-amber-600">is / ’s</span> working.</td>
          </tr>
          <tr>
            <td class="p-2 font-medium text-slate-600 bg-slate-50/50">You / We / They</td>
            <td class="p-2 font-semibold text-slate-900"><span class="text-teal-700">are / ’re</span> eating.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Negative Table -->
    <div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm">
      <div class="bg-slate-100 px-3 py-1.5 font-bold text-slate-700 flex items-center justify-between">
        <span>Negative Statements</span>
        <span class="text-[10px] text-slate-500 font-normal">Subject + Be + Not + Verb-ing</span>
      </div>
      <table class="w-full text-left">
        <tbody class="divide-y divide-slate-100 text-slate-700">
          <tr>
            <td class="p-2 font-medium text-slate-600 bg-slate-50/50 w-2/5">I</td>
            <td class="p-2 font-semibold text-slate-900"><span class="text-rose-600">am not / ’m not</span> studying.</td>
          </tr>
          <tr>
            <td class="p-2 font-medium text-slate-600 bg-slate-50/50">He / She / It</td>
            <td class="p-2 font-semibold text-slate-900"><span class="text-rose-600">is not / isn’t / ’s not</span> working.</td>
          </tr>
          <tr>
            <td class="p-2 font-medium text-slate-600 bg-slate-50/50">You / We / They</td>
            <td class="p-2 font-semibold text-slate-900"><span class="text-rose-600">are not / aren’t / ’re not</span> eating.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Uses of Present Progressive -->
    <div class="bg-slate-50 p-3 rounded-xl border border-slate-200 space-y-1.5 text-slate-700 leading-relaxed">
      <span class="font-bold text-slate-800 block text-[11px] uppercase tracking-wide">Use Present Progressive to talk about:</span>
      <p>• <strong>In progress now (speaking moment):</strong> <em>Look! They’re dancing in the street.</em></p>
      <p>• <strong>In progress at the present time (longer period):</strong> <em>My class is studying world history this semester.</em></p>
    </div>

    <!-- Contrast with Simple Present -->
    <div class="bg-amber-50/70 p-3 rounded-xl border border-amber-200 text-amber-950 space-y-1.5 leading-relaxed">
      <span class="font-bold text-amber-900 block text-[11px] uppercase tracking-wide">Remember: Contrast with Simple Present</span>
      <p>• <strong>Habits & repeated actions:</strong> <em>Dave and I often take a walk after dinner.</em></p>
      <p>• <strong>Facts & general truths:</strong> <em>It snows a lot in Finland.</em></p>
      <p>• <strong>How often something happens:</strong> <em>I meet with my boss twice a week.</em></p>
    </div>

    <!-- Time Expressions & Spelling Note -->
    <div class="p-2.5 bg-slate-50 rounded-xl border border-slate-200 space-y-1 text-slate-700">
      <p><strong>Common Time Expressions:</strong> <em>now, at the moment, right now, this year, these days</em> (e.g. <em>It is raining at the moment. Susie is working hard these days.</em>).</p>
      <p class="text-[11px] text-slate-500 pt-1 border-t border-slate-200 italic">* Sometimes called <em>present continuous</em>. See page A1 for spelling rules (-ing forms).</p>
    </div>
  </div>
</div>"""

CHART_1_5_HTML = """<div class="lg:col-span-5 bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-3">
  <div class="flex items-center justify-between border-b border-slate-100 pb-2">
    <h4 class="font-bold text-slate-900 text-sm sm:text-base">1.5 Present Progressive: Questions & Answers</h4>
    <span class="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-mono">Page 15</span>
  </div>

  <div class="space-y-3 text-xs">
    <!-- Yes/No Questions Table -->
    <div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm">
      <div class="bg-slate-100 px-3 py-1.5 font-bold text-slate-700 flex items-center justify-between">
        <span>Yes / No Questions</span>
        <span class="text-[10px] text-slate-500 font-normal">Short Answers</span>
      </div>
      <div class="p-2.5 bg-white space-y-2 text-slate-700">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-1 border-b border-slate-100 pb-1.5">
          <span><strong>Am</strong> I helping?</span>
          <span class="text-slate-600 font-medium">→ <em>Yes, you are. / No, you’re not (aren't).</em></span>
        </div>
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-1 border-b border-slate-100 pb-1.5">
          <span><strong>Is</strong> he / she / it helping?</span>
          <span class="text-slate-600 font-medium">→ <em>Yes, he is. / No, he’s not (isn't).</em></span>
        </div>
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-1">
          <span><strong>Are</strong> you / we / they helping?</span>
          <span class="text-slate-600 font-medium">→ <em>Yes, we are. / No, we’re not.</em></span>
        </div>
      </div>
    </div>

    <!-- Wh- Questions (Object) Table -->
    <div class="border border-slate-200 rounded-xl overflow-hidden shadow-sm">
      <div class="bg-slate-100 px-3 py-1.5 font-bold text-slate-700 flex items-center justify-between">
        <span>Wh- Questions (Information)</span>
        <span class="text-[10px] text-slate-500 font-normal">Wh- + Be + Subject + Verb-ing</span>
      </div>
      <div class="p-2.5 bg-white space-y-1.5 text-slate-700">
        <p>• <strong>What am</strong> I doing? → <em class="text-slate-900 font-medium">You’re studying.</em></p>
        <p>• <strong>What is</strong> he doing? → <em class="text-slate-900 font-medium">He’s singing.</em></p>
        <p>• <strong>What are</strong> they doing? → <em class="text-slate-900 font-medium">They’re cooking.</em></p>
        <p>• <strong>Why is</strong> she crying? → <em class="text-slate-900 font-medium">She’s watching a sad movie.</em></p>
      </div>
    </div>

    <!-- Who or What as Subject -->
    <div class="border border-amber-200 rounded-xl overflow-hidden bg-amber-50/60 shadow-sm">
      <div class="bg-amber-100/80 px-3 py-1.5 font-bold text-amber-900 flex items-center justify-between">
        <span>Who or What as Subject</span>
        <span class="text-[10px] text-amber-800 font-normal">Who/What + Is + Verb-ing</span>
      </div>
      <div class="p-2.5 space-y-1.5 text-slate-800">
        <div class="flex items-center justify-between">
          <span>• <strong>Who is dancing</strong> with Carmen?</span>
          <span class="text-slate-600 font-medium">→ <em>Her father. / Her father is.</em></span>
        </div>
        <div class="flex items-center justify-between">
          <span>• <strong>What is happening</strong>?</span>
          <span class="text-slate-600 font-medium">→ <em>John’s leaving.</em></span>
        </div>
        <div class="mt-2 pt-2 border-t border-amber-200 text-amber-900 text-[11px] leading-relaxed">
          <p><strong>Remember:</strong> <em>Who</em> or <em>What</em> can be the subject in a Wh- question. When <em>Who</em> or <em>What</em> is the subject, the verb is always in the 3rd person singular form (<em>is + verb-ing</em>):</p>
          <p class="font-medium mt-1">• A: <em>Who’s playing the piano?</em> → B: <em>Marta.</em></p>
        </div>
      </div>
    </div>
  </div>
</div>"""

CHART_1_6_HTML = """<div class="lg:col-span-6 bg-white rounded-2xl border border-slate-200 p-5 reader-card space-y-3">
  <div class="flex items-center justify-between border-b border-slate-100 pb-2">
    <h4 class="font-bold text-slate-900 text-sm sm:text-base">1.6 Action and Non-Action (Stative) Verbs</h4>
    <span class="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-mono">Page 16</span>
  </div>

  <!-- Rule 1: Action Verbs -->
  <div class="p-2.5 bg-slate-50 rounded-xl border border-slate-200 text-xs text-slate-700">
    <strong>1. Action verbs</strong> describe physical or mental actions:
    <div class="mt-1 flex flex-wrap gap-4 text-slate-800 font-medium">
      <span>• <em>Action:</em> She studies hard every night.</span>
      <span>• <em>Non-Action:</em> I want to go to the dance.</span>
    </div>
  </div>

  <!-- Rule 2: Non-Action Categories -->
  <div class="space-y-1 text-xs">
    <p class="text-slate-700 font-semibold">2. Non-action verbs describe states, conditions, or feelings (not actions):</p>
    <div class="grid grid-cols-2 sm:grid-cols-3 gap-2">
      <div class="p-2 bg-slate-50 rounded-lg border border-slate-200">
        <strong class="text-slate-800 block mb-0.5">Feelings</strong>
        <p class="text-slate-600 font-medium">dislike, hate, like, love, miss</p>
        <p class="text-[11px] text-teal-700 italic mt-0.5">I love to dance.</p>
      </div>
      <div class="p-2 bg-slate-50 rounded-lg border border-slate-200">
        <strong class="text-slate-800 block mb-0.5">Senses</strong>
        <p class="text-slate-600 font-medium">feel, hear, see, smell, sound, taste</p>
        <p class="text-[11px] text-teal-700 italic mt-0.5">The soup smells delicious.</p>
      </div>
      <div class="p-2 bg-slate-50 rounded-lg border border-slate-200">
        <strong class="text-slate-800 block mb-0.5">Possession</strong>
        <p class="text-slate-600 font-medium">belong, have, own</p>
        <p class="text-[11px] text-teal-700 italic mt-0.5">He doesn’t own a car.</p>
      </div>
      <div class="p-2 bg-slate-50 rounded-lg border border-slate-200">
        <strong class="text-slate-800 block mb-0.5">Appearance</strong>
        <p class="text-slate-600 font-medium">appear, look, seem</p>
        <p class="text-[11px] text-teal-700 italic mt-0.5">Ted looks tired today.</p>
      </div>
      <div class="p-2 bg-slate-50 rounded-lg border border-slate-200">
        <strong class="text-slate-800 block mb-0.5">Desires</strong>
        <p class="text-slate-600 font-medium">hope, need, prefer, want</p>
        <p class="text-[11px] text-teal-700 italic mt-0.5">I want some coffee.</p>
      </div>
      <div class="p-2 bg-slate-50 rounded-lg border border-slate-200">
        <strong class="text-slate-800 block mb-0.5">Mental States</strong>
        <p class="text-slate-600 font-medium">believe, think, understand</p>
        <p class="text-[11px] text-teal-700 italic mt-0.5">She understands Japanese.</p>
      </div>
    </div>
  </div>

  <!-- Rule 3: Progressive Prohibition -->
  <div class="p-2.5 bg-slate-50 rounded-xl border border-slate-200 text-xs text-slate-700 flex flex-wrap items-center justify-between gap-2">
    <div><strong>3. Progressive form:</strong> Non-action verbs are not usually used in progressive.</div>
    <div class="flex items-center gap-3 font-mono text-[11px]">
      <span class="text-emerald-800">✓ They own a house.</span>
      <span class="text-rose-600">✗ They are owning a house.</span>
    </div>
  </div>

  <!-- Rule 4: Meaning Shift -->
  <div class="border border-amber-200 rounded-xl p-3 bg-amber-50/70 text-xs text-amber-950 space-y-1.5">
    <span class="font-bold block text-amber-900">4. Meaning Shifts with Progressive:</span>
    <p class="text-slate-700">Some non-action verbs can be used in progressive, but their meaning changes:</p>
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 mt-1">
      <div class="bg-white/80 p-2 rounded border border-amber-100">
        <strong class="text-amber-900 block font-mono">• have:</strong>
        <p class="text-slate-600"><em>Non-action (possession):</em> He has a headache.</p>
        <p class="text-slate-600"><em>Action (eating/experiencing):</em> He is having lunch.</p>
      </div>
      <div class="bg-white/80 p-2 rounded border border-amber-100">
        <strong class="text-amber-900 block font-mono">• think:</strong>
        <p class="text-slate-600"><em>Non-action (opinion):</em> I think this book is great.</p>
        <p class="text-slate-600"><em>Action (mental process):</em> I am thinking of the answer.</p>
      </div>
      <div class="bg-white/80 p-2 rounded border border-amber-100">
        <strong class="text-amber-900 block font-mono">• taste:</strong>
        <p class="text-slate-600"><em>Non-action (property):</em> The food tastes good.</p>
        <p class="text-slate-600"><em>Action (act of tasting):</em> She is tasting the food.</p>
      </div>
      <div class="bg-white/80 p-2 rounded border border-amber-100">
        <strong class="text-amber-900 block font-mono">• look & smell:</strong>
        <p class="text-slate-600"><em>Non-action:</em> Ted looks tired. / Soup smells good.</p>
        <p class="text-slate-600"><em>Action:</em> He is looking at photos. / She is smelling flowers.</p>
      </div>
    </div>
  </div>
</div>"""

GRAMMAR_FOCUS_HTML = """<div class="bg-teal-50 rounded-xl border border-teal-200 p-4 text-xs text-teal-950 space-y-1.5">
  <span class="font-bold text-teal-900 block text-xs uppercase tracking-wide">GRAMMAR FOCUS: Simple Present for Facts & Repeated Activities (Page 22)</span>
  <p class="text-slate-700">In the model text, the writer uses the <strong>simple present</strong> to talk about repeated activities, events, and facts:</p>
  <div class="space-y-1 text-slate-800 font-medium pl-2 border-l-2 border-teal-500">
    <p>• <em>In February, my family and I usually go to the Kila Raipur Sports Festival.</em></p>
    <p>• <em>Kila Raipur is a town near my home in India.</em></p>
    <p>• <em>At the festival, people race huge tractors. Men sometimes lift bicycles with their teeth.</em></p>
  </div>
</div>"""

def find_chart_card(soup, prefix):
    for c in soup.select('.reader-card'):
        h = c.find(['h2', 'h3', 'h4', 'h5'])
        if h and prefix in h.get_text():
            return c
    return None

def update_u1_all_in_one():
    fpath = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 1/GE2 - U1.html'
    soup = BeautifulSoup(open(fpath, encoding='utf-8'), 'html.parser')
    
    # 1.1
    c11 = find_chart_card(soup, '1.1')
    if c11:
        new_tag = BeautifulSoup(CHART_1_1_HTML, 'html.parser').find(class_='reader-card')
        c11.replace_with(new_tag)
        print("  + Replaced Chart 1.1 in GE2 - U1.html")
        
    # 1.2
    c12 = find_chart_card(soup, '1.2')
    if c12:
        new_tag = BeautifulSoup(CHART_1_2_HTML, 'html.parser').find(class_='reader-card')
        c12.replace_with(new_tag)
        print("  + Replaced Chart 1.2 in GE2 - U1.html")

    # 1.3
    c13 = find_chart_card(soup, '1.3')
    if c13:
        new_tag = BeautifulSoup(CHART_1_3_HTML, 'html.parser').find(class_='reader-card')
        c13.replace_with(new_tag)
        print("  + Replaced Chart 1.3 in GE2 - U1.html")

    # 1.4
    c14 = find_chart_card(soup, '1.4')
    if c14:
        new_tag = BeautifulSoup(CHART_1_4_HTML, 'html.parser').find(class_='reader-card')
        c14.replace_with(new_tag)
        print("  + Replaced Chart 1.4 in GE2 - U1.html")

    # 1.5
    c15 = find_chart_card(soup, '1.5')
    if c15:
        new_tag = BeautifulSoup(CHART_1_5_HTML, 'html.parser').find(class_='reader-card')
        c15.replace_with(new_tag)
        print("  + Replaced Chart 1.5 in GE2 - U1.html")

    # 1.6
    c16 = find_chart_card(soup, '1.6')
    if c16:
        new_tag = BeautifulSoup(CHART_1_6_HTML, 'html.parser').find(class_='reader-card')
        c16.replace_with(new_tag)
        print("  + Replaced Chart 1.6 in GE2 - U1.html")

    # Grammar Focus in Model Reading
    for c in soup.select('#tab-writing .reader-card'):
        if 'Kila Raipur' in c.get_text():
            # Check if GRAMMAR FOCUS already exists
            if not c.find(text=re.compile('GRAMMAR FOCUS')):
                writing_focus = c.find(text=re.compile('WRITING FOCUS'))
                gf_tag = BeautifulSoup(GRAMMAR_FOCUS_HTML, 'html.parser')
                if writing_focus:
                    # Find parent box of writing focus and insert before it
                    wf_box = writing_focus.find_parent(class_=lambda x: x and 'rounded-xl' in x)
                    if wf_box:
                        wf_box.insert_before(gf_tag)
                    else:
                        c.append(gf_tag)
                else:
                    c.append(gf_tag)
                print("  + Added GRAMMAR FOCUS to Model Reading in GE2 - U1.html")
            break

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("[SUCCESS] GE2 - U1.html updated!")

def update_u1_lesson_1():
    fpath = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 1/grammar_explorer_2_unit_1_lesson_1.html'
    soup = BeautifulSoup(open(fpath, encoding='utf-8'), 'html.parser')

    c11 = find_chart_card(soup, '1.1')
    if c11:
        new_tag = BeautifulSoup(CHART_1_1_HTML, 'html.parser').find(class_='reader-card')
        c11.replace_with(new_tag)
        print("  + Replaced Chart 1.1 in grammar_explorer_2_unit_1_lesson_1.html")

    c12 = find_chart_card(soup, '1.2')
    if c12:
        new_tag = BeautifulSoup(CHART_1_2_HTML, 'html.parser').find(class_='reader-card')
        c12.replace_with(new_tag)
        print("  + Replaced Chart 1.2 in grammar_explorer_2_unit_1_lesson_1.html")

    c13 = find_chart_card(soup, '1.3')
    if c13:
        new_tag = BeautifulSoup(CHART_1_3_HTML, 'html.parser').find(class_='reader-card')
        c13.replace_with(new_tag)
        print("  + Replaced Chart 1.3 in grammar_explorer_2_unit_1_lesson_1.html")

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("[SUCCESS] grammar_explorer_2_unit_1_lesson_1.html updated!")

def update_u1_lesson_2():
    fpath = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 1/grammar_explorer_2_unit_1_lesson_2.html'
    soup = BeautifulSoup(open(fpath, encoding='utf-8'), 'html.parser')

    c14 = find_chart_card(soup, '1.4')
    if c14:
        new_tag = BeautifulSoup(CHART_1_4_HTML, 'html.parser').find(class_='reader-card')
        c14.replace_with(new_tag)
        print("  + Replaced Chart 1.4 in grammar_explorer_2_unit_1_lesson_2.html")

    c15 = find_chart_card(soup, '1.5')
    if c15:
        new_tag = BeautifulSoup(CHART_1_5_HTML, 'html.parser').find(class_='reader-card')
        c15.replace_with(new_tag)
        print("  + Replaced Chart 1.5 in grammar_explorer_2_unit_1_lesson_2.html")

    c16 = find_chart_card(soup, '1.6')
    if c16:
        new_tag = BeautifulSoup(CHART_1_6_HTML, 'html.parser').find(class_='reader-card')
        c16.replace_with(new_tag)
        print("  + Replaced Chart 1.6 in grammar_explorer_2_unit_1_lesson_2.html")

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("[SUCCESS] grammar_explorer_2_unit_1_lesson_2.html updated!")

def update_u1_review_writing():
    fpath = 'Grammar-Explorer-book/Grammar-Explorer-2/Unit 1/grammar_explorer_2_unit_1_review_writing.html'
    soup = BeautifulSoup(open(fpath, encoding='utf-8'), 'html.parser')

    # Grammar Focus in Model Reading
    for c in soup.select('.reader-card'):
        if 'Kila Raipur' in c.get_text():
            if not c.find(text=re.compile('GRAMMAR FOCUS')):
                writing_focus = c.find(text=re.compile('WRITING FOCUS'))
                gf_tag = BeautifulSoup(GRAMMAR_FOCUS_HTML, 'html.parser')
                if writing_focus:
                    wf_box = writing_focus.find_parent(class_=lambda x: x and 'rounded-xl' in x)
                    if wf_box:
                        wf_box.insert_before(gf_tag)
                    else:
                        c.append(gf_tag)
                else:
                    c.append(gf_tag)
                print("  + Added GRAMMAR FOCUS to Model Reading in grammar_explorer_2_unit_1_review_writing.html")
            break

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("[SUCCESS] grammar_explorer_2_unit_1_review_writing.html updated!")

if __name__ == '__main__':
    print("Executing Unit 1 Grammar Content Updates...")
    update_u1_all_in_one()
    update_u1_lesson_1()
    update_u1_lesson_2()
    update_u1_review_writing()
    print("All Unit 1 grammar updates completed!")
