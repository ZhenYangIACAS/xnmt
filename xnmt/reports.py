import matplotlib.pyplot as plt
import numpy as np
import dynet as dy
import os

class Report(object):

  def write_report(self, path_to_report, idx=None):
    '''write the report to the given path.

     Parameters:
     path_to_report => path to output the report
    '''
 
class DefaultTranslatorReport(Report): 

  def __init__(self):
    self.src_text = None
    self.trg_text = None
    self.src_words = None
    self.trg_words = None
    self.attentions = None
    self.hidden_states = None

  @staticmethod
  def plot_attention(src_words, trg_words, attention_matrix, file_name=None):
    """This takes in source and target words and an attention matrix (in numpy format)
    and prints a visualization of this to a file.
    :param src_words: a list of words in the source
    :param trg_words: a list of target words
    :param attention_matrix: a two-dimensional numpy array of values between zero and one,
      where rows correspond to source words, and columns correspond to target words
    :param file_name: the name of the file to which we write the attention
    """
    fig, ax = plt.subplots()

    # put the major ticks at the middle of each cell
    ax.set_xticks(np.arange(attention_matrix.shape[1]) + 0.5, minor=False)
    ax.set_yticks(np.arange(attention_matrix.shape[0]) + 0.5, minor=False)
    ax.invert_yaxis()

    # label axes by words
    ax.set_xticklabels(trg_words, minor=False)
    ax.set_yticklabels(src_words, minor=False)
    ax.xaxis.tick_top()

    # draw the heatmap
    plt.pcolor(attention_matrix, cmap=plt.cm.Blues, vmin=0, vmax=1)
    plt.colorbar()

    if file_name != None:
        plt.savefig(file_name, dpi=100)
    else:
        plt.show()
    plt.close()
    
  def write_report(self, path_to_report, idx=None):
    filename_of_report = os.path.basename(path_to_report)
    with open("{}.html".format(path_to_report), 'w') as f:
      if idx != None:
        f.write("<html><head><title>Translation Report for Sentence {}</title></head><body>\n".format(idx))
        f.write("<h1>Translation Report for Sentence {}</h1>\n".format(idx))
      else:
        f.write("<html><head><title>Translation Report</title></head><body>\n")
        f.write("<h1>Translation Report</h1>\n")
      src_text, trg_text = None, None
      # Print Source text
      if self.src_text != None: f.write("<p><b>Source Text: </b> {}</p>\n".format(self.src_text))
      if self.src_words != None: f.write("<p><b>Source Words: </b> {}</p>\n".format(' '.join(self.src_words)))
      if self.trg_text != None: f.write("<p><b>Target Text: </b> {}</p>\n".format(self.trg_text))
      if self.trg_words != None: f.write("<p><b>Target Words: </b> {}</p>\n".format(' '.join(self.trg_words)))
      # Alignments
      if  all([x != None for x in [self.src_words, self.trg_words, self.attentions]]):
        if type(self.attentions) == dy.Expression:
          self.attentions = self.attentions.npvalue()
        elif type(self.attentions) == list:
          self.attentions = np.concatenate([x.npvalue() for x in self.attentions], axis=1)
        elif type(self.attentions) != np.ndarray:
          raise RuntimeError("Illegal type for attentions in translator report: {}".format(type(self.attentions)))
        attention_file = "{}.attention.png".format(path_to_report)
        DefaultTranslatorReport.plot_attention(self.src_words, self.trg_words, self.attentions, file_name = attention_file)
        f.write("<p><b>Attention:</b><br/><img src=\"{}.attention.png\"/></p>\n".format(filename_of_report))

      f.write("</body></html>")

    #for i in len(self.hidden_states)
    print("\n{}.hidden_states".format(path_to_report) , self.hidden_states['l1'].npvalue(), '\n')
    print('\n shape is ', self.hidden_states['l1'].npvalue().shape)
    #  TODO:
    # save the hidden states in .npz, following the same structure as the dev input
    # to make sure how we deal with the shape, flatten ? or else.

class DefaultRetrieverReport(Report):
    
    def __init__(self):
      self.hidden_states = None

    def write_report(self, path_to_report, idx=None):
      filename_of_report = os.path.basename(path_to_report)
      print("\n{}.hidden_states".format(path_to_report) , self.hidden_states['l1'].npvalue(), '\n')
      print('\n shape is ', self.hidden_states['l1'].npvalue().shape)
      print('\n ', filename_of_report)


if __name__ == "__main__":

  # temporary call to plot_attention
  rep = DefaultTranslatorReport()
  rep.src_words = ['The', 'cat', 'was', 'sitting', 'on', 'top', 'of', 'the', 'wardrobe', '.']
  rep.trg_words = ['Le', 'chat', 'etait', 'assis', 'sur', 'le', 'dessus', 'de', 'l\'armoire', '.']
  rep.attentions = np.random.rand(len(rep.src_words), len(rep.trg_words))
  
  rep.write_report("/tmp/xnmt_translator_report", 1)
